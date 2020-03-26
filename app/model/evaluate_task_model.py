# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-4:54 下午
from abc import ABC
from sqlalchemy import not_
from app.model.base import BaseModel
from app.entity.evaluate_task import EvaluateTask

from app.common.extension import session


class EvaluateTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(EvaluateTask).filter(not_(EvaluateTask.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(EvaluateTask).filter(EvaluateTask.evaluate_task_id == _id,
                                                  not_(EvaluateTask.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_task_id"]
        # Compose query
        q = session.query(EvaluateTask).filter(not_(EvaluateTask.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(EvaluateTask, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: EvaluateTask) -> EvaluateTask:
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(EvaluateTask).filter(EvaluateTask.doc_type_id == _id).update({EvaluateTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass
