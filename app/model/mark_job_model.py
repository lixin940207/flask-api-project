from abc import ABC

from sqlalchemy import not_

from app.model.base import BaseModel
from app.entity.mark_job import MarkJob
from app.common.extension import session


class MarkJobModel(BaseModel, ABC):
    def get_all(self):
        raise NotImplemented("no get_all")
        # return session.query(MarkJob).filter(not_(MarkJob.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(MarkJob).filter(MarkJob.mark_job_id == _id, not_(MarkJob.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(MarkJob).filter(not_(MarkJob.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkJob, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity):
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(MarkJob).filter(MarkJob.mark_job_id == _id).update({MarkJob.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(MarkJob).filter(MarkJob.mark_job_id.in_(_id_list)).update({MarkJob.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        raise NotImplemented("no bulk_update")
