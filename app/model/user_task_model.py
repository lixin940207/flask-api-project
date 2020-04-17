from abc import ABC

from flask_restful import abort
from sqlalchemy import not_, func

from app.common.common import StatusEnum, RoleEnum, Common
from app.common.filters import CurrentUser
from app.common.utils.status_mapper import status_str2int_mapper
from app.model.base import BaseModel
from app.entity import UserTask, MarkTask, DocType, Doc, MarkJob
from app.common.extension import session


class UserTaskModel(BaseModel, ABC):
    def get_all(self):
        raise NotImplemented("no get_all")

    @staticmethod
    def is_empty_table():
        return session.query(UserTask).filter(not_(UserTask.is_deleted)).count() == 0

    def get_by_id(self, _id):
        return session.query(UserTask).filter(UserTask.user_task_id == _id, not_(UserTask.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["mark_task_id", "annotator_id", "user_task_status"]
        # Compose query
        q = session.query(UserTask).filter(~UserTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(UserTask, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(UserTask, order_by).desc())
        else:
            q = q.order_by(getattr(UserTask, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs):
        entity = UserTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        entity_list = [UserTask(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(UserTask).filter(UserTask.user_task_id == _id).update({UserTask.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(UserTask).filter(UserTask.user_task_id.in_(_id_list)).update({UserTask.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, _id, **kwargs) -> UserTask:
        entity = session.query(UserTask).filter(UserTask.user_task_id == _id)
        entity.update(kwargs)
        session.flush()
        return entity.one()

    def bulk_update(self, _id_list, **kwargs):
        entity_list = session.query(UserTask).filter(UserTask.user_task_id.in_(_id_list))
        entity_list.update(kwargs, synchronize_session="fetch")
        session.flush()
        return entity_list.all()

    @staticmethod
    def update_status_to_unlabel_by_mark_task_id(mark_task_id):
        q = session.query(UserTask).filter(
            UserTask.mark_task_id == mark_task_id,
            ~UserTask.is_deleted
        )
        if q.all():
            q.update({UserTask.user_task_status: int(StatusEnum.unlabel)}, synchronize_session='fetch')
        else:
            abort(400, message="无法驳回无标注员任务")
        session.flush()

    @staticmethod
    def get_user_task_with_doc_and_doc_type(nlp_task_id, current_user: CurrentUser, args):
        q = session.query(UserTask, DocType, Doc) \
            .join(MarkTask, MarkTask.mark_task_id == UserTask.mark_task_id) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .join(Doc, Doc.doc_id == MarkTask.doc_id) \
            .filter(
            DocType.nlp_task_id == nlp_task_id,
            ~UserTask.is_deleted,
            ~MarkTask.is_deleted,
            ~Doc.is_deleted
        )
        # TODO
        # 权限
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value]:
            q = q.filter(func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id)))
        elif current_user.user_role in [RoleEnum.annotator.value]:
            # q = q.filter(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))
            q = q.filter(UserTask.annotator_id == current_user.user_id)
        if args.get('job_id'):
            q = q.filter(MarkTask.mark_job_id == args['job_id'])
        if args.get('doc_type_id'):
            q = q.filter(MarkJob.doc_type_id == args['doc_type_id'])
        if args['task_state']:
            q = q.filter(MarkTask.mark_task_status == status_str2int_mapper().get(args['task_state']))
        if args['query']:
            q = q.filter(Doc.doc_raw_name.like(f'%{args["query"]}%'))
        q = q.group_by(UserTask)
        count = q.count()
        processing_count = q.filter(MarkTask.mark_task_status == int(StatusEnum.processing)).count()
        if args['order_by'] and isinstance(args['order_by'], str):
            if args['order_by'][1:] == 'task_id':
                args['order_by'] = args['order_by'][0] + 'mark_task_id'
            q = Common().order_by_model_fields(q, UserTask, [args['order_by']])
        items = []
        for user_task, doc_type, doc in q.offset(args['offset']).limit(args['limit']).all():
            user_task.doc = doc
            user_task.doc_type = doc_type
            items.append(user_task)
        return count, count - processing_count, items

    @staticmethod
    def get_user_task_with_doc_and_user_task_list_by_id(task_id):
        user_task, mark_task, doc, doc_type = session.query(UserTask, MarkTask, Doc, DocType) \
            .join(MarkTask, MarkTask.mark_task_id == UserTask.mark_task_id) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .join(Doc, Doc.doc_id == MarkTask.doc_id) \
            .filter(
            UserTask.user_task_id == task_id,
            ~UserTask.is_deleted,
            ~Doc.is_deleted
        ).one()
        user_task.doc = doc
        user_task.doc_type = doc_type
        return user_task

    @staticmethod
    def get_preview_and_next_user_task_id(current_user, nlp_task_id, task_id, args):
        q = session.query(UserTask.user_task_id) \
            .join(MarkTask, MarkTask.mark_task_id == UserTask.mark_task_id) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .filter(
            DocType.nlp_task_id == nlp_task_id,
            UserTask.user_task_status != int(StatusEnum.processing),
            ~MarkTask.is_deleted,
            ~UserTask.is_deleted,
        )

        if args.get('job_id'):
            q = q.filter(MarkJob.mark_job_id == args['job_id'])
        if args.get("task_state"):
            q = q.filter(UserTask.user_task_status == args.get("task_state"))
        if args.get("query"):
            q = q.filter(Doc.doc_raw_name.contains(args.get("query")))

        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value]:
            q = q.filter(func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id)))
        elif current_user.user_role in [RoleEnum.annotator.value]:
            # q = q.filter(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))
            q = q.filter(UserTask.annotator_ids == current_user.user_id)

        q1 = Common().order_by_model_fields(q.filter(UserTask.user_task_id < task_id), UserTask, ['-user_task_id'])
        q2 = Common().order_by_model_fields(q.filter(UserTask.user_task_id > task_id), UserTask, ['+user_task_id'])

        next_task_id = q1.limit(1).first()
        preview_task_id = q2.limit(1).first()
        return preview_task_id[0] if preview_task_id else None, next_task_id[0] if next_task_id else None

