# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-5:01 下午
from abc import ABC
from sqlalchemy import not_
from app.model.base import BaseModel
from app.entity.train_term_task import TrainTermTask

from app.common.extension import session


class TrainTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainTermTask).filter(not_(TrainTermTask.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(TrainTermTask).filter(TrainTermTask.train_term_task_id == _id,
                                                   not_(TrainTermTask.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_task_id", "doc_term_id"]
        # Compose query
        q = session.query(TrainTermTask).filter(not_(TrainTermTask.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTermTask, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: TrainTermTask) -> TrainTermTask:
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(TrainTermTask).filter(TrainTermTask.doc_type_id == _id).update({TrainTermTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass
