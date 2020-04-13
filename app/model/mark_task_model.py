from abc import ABC
from sqlalchemy import not_, func
from typing import List, Tuple, Dict

from app.common.filters import CurrentUser
from app.common.common import StatusEnum, RoleEnum
from app.entity import DocType, MarkJob, Doc
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

    def get_mark_task_and_doc_by_mark_job_ids(self, mark_job_ids):
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

    def update(self, entity):
        pass

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
            q = q.filter(func.json_contains(MarkJob.reviewer_ids, current_user.user_id))
        elif current_user.user_role in [RoleEnum.annotator.value]:
            q = q.filter(func.json_contains(MarkJob.annotator_ids, current_user.user_id))
        # get grouped (doc_type_id, mark_job_id, count) list
        all_status = q.group_by(MarkJob.doc_type_id, MarkJob.mark_job_id) \
            .with_entities(DocType.doc_type_id, MarkJob.mark_job_id, func.count(MarkTask.mark_task_id)).all()
        # filter >= labeled status
        q = q.filter(MarkTask.mark_task_status >= int(StatusEnum.labeled))
        # get grouped (doc_type_id, mark_job_id, >= labeled count) list
        all_finish_marking_status = q.group_by(MarkJob.doc_type_id, MarkJob.mark_job_id) \
            .with_entities(DocType.doc_type_id, MarkJob.mark_job_id, func.count(MarkTask.mark_task_id)).all()
        return all_status, all_finish_marking_status

    @staticmethod
    def get_mark_job_id_by_id(_id):
        q = session.query(MarkTask).filter(MarkTask.mark_task_id == _id).one()
        return q.mark_job_id

    @staticmethod
    def update_status_to_unlabel_by_manual_task_id(_id):
        q = session.query(MarkTask).filter(MarkTask.mark_task_id == _id).one()
        q.mark_task_result = []
        q.mark_task_status = int(StatusEnum.unlabel)
