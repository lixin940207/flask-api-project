# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-3:40 下午
from abc import ABC
from sqlalchemy import not_
from app.model.base import BaseModel
from app.entity.train_task import TrainTask

from app.common.extension import session


class TrainTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainTask).filter(not_(TrainTask.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(TrainTask).filter(TrainTask.train_task_id == _id, not_(TrainTask.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_id"]
        # Compose query
        q = session.query(TrainTask).filter(not_(TrainTask.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTask, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: TrainTask) -> TrainTask:
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(TrainTask).filter(TrainTask.doc_type_id == _id).update({TrainTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass
