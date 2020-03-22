from abc import ABC

from sqlalchemy import not_

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

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
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

    def create(self, entity: MarkTask) -> MarkTask:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: [MarkTask]) -> [MarkTask]:
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
