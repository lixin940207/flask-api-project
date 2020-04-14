from abc import ABC

from sqlalchemy import not_, func
from typing import List, Tuple

from app.common.filters import CurrentUser
from app.common.common import StatusEnum, RoleEnum, Common
from app.common.utils.status_mapper import status_str2int_mapper
from app.entity import DocType, MarkJob, Doc, UserTask
from app.model.base import BaseModel
from app.entity.mark_task import MarkTask
from app.common.extension import session


class MarkTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(MarkTask).filter(not_(MarkTask.is_deleted)).all()

    @staticmethod
    def is_empty_table():
        return session.query(MarkTask).filter(not_(MarkTask.is_deleted)).count() == 0

    def get_by_id(self, _id):
        return session.query(MarkTask).filter(MarkTask.mark_task_id == _id, not_(MarkTask.is_deleted)).one()

    def get_unlabel_tasks_by_mark_job_ids(self, mark_job_ids):
        """根据mark job获取所有未标注的mark task"""
        unlabel_tasks = session.query(
            UserTask.mark_task_id, Doc.doc_id, Doc.doc_unique_name, DocType.doc_type_id, MarkJob.mark_job_type
        ).join(
            MarkTask, MarkTask.mark_task_id == UserTask.mark_task_id
        ).join(
            Doc, Doc.doc_id == MarkTask.doc_id
        ).join(
            MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id
        ).join(
            DocType, DocType.doc_type_id == MarkJob.doc_type_id
        ).filter(
            MarkJob.mark_job_id.in_(mark_job_ids),
            UserTask.user_task_status.notin_(
                [int(x) for x in [StatusEnum.labeled, StatusEnum.approved, StatusEnum.reviewing, StatusEnum.processing]]
            ),
            ~UserTask.is_deleted,
            ~MarkTask.is_deleted,
            ~Doc.is_deleted,
            ~MarkJob.is_deleted,
            ~DocType.is_deleted,
        ).all()
        return unlabel_tasks

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["mark_job_id", "doc_id", "reviewer_id", "mark_task_status"]
        # Compose query
        q = session.query(MarkTask).filter(not_(MarkTask.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkTask, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def get_mark_task_and_doc_by_mark_job_ids(self, mark_job_ids) -> List[Tuple[MarkTask, Doc]]:
        """获取已审核数据"""
        q = session.query(MarkTask, Doc) \
            .join(Doc, Doc.doc_id == MarkTask.doc_id) \
            .join(MarkJob, MarkTask.mark_job_id == MarkJob.mark_job_id) \
            .filter(
            MarkJob.mark_job_id.in_(mark_job_ids),
            MarkTask.mark_task_status == int(StatusEnum.approved),
            ~MarkJob.is_deleted,
            ~Doc.is_deleted,
            ~MarkTask.is_deleted)
        return q.all()

    def create(self, **kwargs) -> MarkTask:
        entity = MarkTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: List[dict]) -> List[MarkTask]:
        entity_list = [MarkTask(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(MarkTask).filter(MarkTask.mark_task_id == _id).update({MarkTask.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(MarkTask).filter(MarkTask.mark_task_id.in_(_id_list)).update({MarkTask.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, _id, **kwargs) -> MarkTask:
        entity = session.query(MarkTask).filter(MarkTask.mark_task_id == _id)
        entity.update(kwargs)
        session.flush()
        return entity.one()

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(MarkTask, entity_list)

    @staticmethod
    def count_mark_task_status(mark_job_ids) -> [Tuple[int]]:
        all_count = session.query(
            MarkTask.mark_job_id, MarkTask.mark_task_status, func.count(MarkTask.mark_task_status)) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .filter(MarkJob.mark_job_id.in_(mark_job_ids),
                    ~MarkTask.is_deleted, ~MarkJob.is_deleted) \
            .group_by(MarkTask.mark_task_status, MarkTask.mark_job_id).all()
        return all_count

    @staticmethod
    def count_status_by_user(nlp_task_id, current_user: CurrentUser):
        # compose query
        q = session.query(DocType) \
            .join(MarkJob, DocType.doc_type_id == MarkJob.doc_type_id)\
            .join(MarkTask, MarkJob.mark_job_id == MarkTask.mark_job_id)\
            .filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~MarkJob.is_deleted, ~MarkTask.is_deleted)
        # filter by user
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value]:
            q = q.filter(func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id)))
        elif current_user.user_role in [RoleEnum.annotator.value]:
            q = q.filter(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))
        # get grouped (doc_type_id, mark_job_id, count) list
        all_status = q.group_by(MarkJob.doc_type_id, MarkJob.mark_job_id) \
            .with_entities(MarkJob.doc_type_id, MarkJob.mark_job_id, func.count(MarkTask.mark_task_id)).all()
        # filter >= labeled status
        q = q.filter(MarkTask.mark_task_status >= int(StatusEnum.labeled))
        # get grouped (doc_type_id, mark_job_id, >= labeled count) list
        all_finish_marking_status = q.group_by(MarkJob.doc_type_id, MarkJob.mark_job_id) \
            .with_entities(MarkJob.doc_type_id, MarkJob.mark_job_id, func.count(MarkTask.mark_task_id)).all()
        return all_status, all_finish_marking_status

    @staticmethod
    def get_mark_job_id_by_id(_id):
        q = session.query(MarkTask).filter(MarkTask.mark_task_id == _id).one()
        return q.mark_job_id

    @staticmethod
    def update_status_to_unlabel_by_mark_task_id(_id):
        q = session.query(MarkTask).filter(MarkTask.mark_task_id == _id).one()
        q.mark_task_result = []
        q.mark_task_status = int(StatusEnum.unlabel)

    def get_mark_task_with_doc_and_doc_type(self, nlp_task_id, current_user: CurrentUser, args):
        q = session.query(MarkTask, DocType, Doc) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .join(Doc, Doc.doc_id == MarkTask.doc_id) \
            .filter(
            DocType.nlp_task_id == nlp_task_id,
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
            q = q.filter(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))
        if args.get('job_id'):
            q = q.filter(MarkTask.mark_job_id == args['job_id'])
        if args.get('doc_type_id'):
            q = q.filter(MarkJob.doc_type_id == args['doc_type_id'])
        if args['task_state']:
            q = q.filter(MarkTask.mark_task_status == status_str2int_mapper().get(args['task_state']))
        if args['query']:
            q = q.filter(Doc.doc_raw_name.like(f'%{args["query"]}%'))
        q = q.group_by(MarkTask)
        count = q.count()
        processing_count = q.filter(MarkTask.mark_task_status == int(StatusEnum.processing)).count()
        if args['order_by'] and isinstance(args['order_by'], str):
            if args['order_by'][1:] == 'task_id':
                args['order_by'] = args['order_by'][0] + 'mark_task_id'
            q = Common().order_by_model_fields(q, MarkTask, [args['order_by']])
        items = []
        results = q.offset(args['offset']).limit(args['limit']).all()
        mark_task_ids = [mark_task.mark_task_id for mark_task, _, _ in results]
        user_task_map = self._get_user_task_map(mark_task_ids, select_keys=(UserTask))   #.annotator_id, UserTask.mark_task_id))
        for mark_task, doc_type, doc in q.offset(args['offset']).limit(args['limit']).all():
            user_task_list = user_task_map[str(mark_task.mark_task_id)]
            mark_task.user_task_list = user_task_list
            mark_task.doc = doc
            mark_task.doc_type = doc_type
            items.append(mark_task)
        return count, count - processing_count, items

    @staticmethod
    def get_mark_task_with_doc_and_user_task_list_by_id(task_id):
        mark_task, doc, doc_type = session.query(MarkTask, Doc, DocType) \
            .join(Doc, Doc.doc_id == MarkTask.doc_id) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .filter(
            MarkTask.mark_task_id == task_id,
            ~MarkTask.is_deleted,
            ~Doc.is_deleted
        ).one()
        mark_task.doc = doc
        mark_task.doc_type = doc_type
        mark_task.user_task_list = session.query(UserTask).filter(
            UserTask.mark_task_id == task_id,
            ~UserTask.is_deleted
        ).all()
        return mark_task

    @staticmethod
    def _get_user_task_map(mark_task_ids, select_keys):  # tuple):
        """select_keys必须包含mark_task_id"""
        user_tasks = session.query(select_keys).filter(UserTask.mark_task_id.in_(mark_task_ids)).all()
        user_task_map = {}
        for user_task in user_tasks:
            mark_task_id_key = str(user_task.mark_task_id)
            if user_task_map.get(mark_task_id_key):
                user_task_map[mark_task_id_key].append(user_task)
            else:
                user_task_map[mark_task_id_key] = [user_task]
        return user_task_map
    
    @staticmethod
    def get_preview_and_next_mark_task_id(current_user, nlp_task_id, task_id, args):
        q = session.query(MarkTask.mark_task_id) \
            .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
            .join(MarkJob, MarkJob.mark_job_id == MarkTask.mark_job_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .filter(
            DocType.nlp_task_id == nlp_task_id,
            MarkTask.mark_task_status != int(StatusEnum.processing),
            ~MarkTask.is_deleted,
            ~UserTask.is_deleted,
        )

        if args.get('job_id'):
            q = q.filter(MarkJob.mark_job_id == args['job_id'])
        if args.get("task_state"):
            q = q.filter(MarkTask.mark_task_status == args.get("task_state"))
        if args.get("query"):
            q = q.filter(Doc.doc_raw_name.contains(args.get("query")))

        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value]:
            q = q.filter(func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id)))
        elif current_user.user_role in [RoleEnum.annotator.value]:
            q = q.filter(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))

        q1 = Common().order_by_model_fields(q.filter(MarkTask.mark_task_id < task_id), MarkTask, ['-mark_task_id'])
        q2 = Common().order_by_model_fields(q.filter(MarkTask.mark_task_id > task_id), MarkTask, ['+mark_task_id'])

        next_task_id = q1.limit(1).first()
        preview_task_id = q2.limit(1).first()
        return preview_task_id[0] if preview_task_id else None, next_task_id[0] if next_task_id else None
