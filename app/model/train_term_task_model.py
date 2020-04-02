# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-5:01 下午
from abc import ABC
from app.entity import TrainTask
from app.model.base import BaseModel
from app.entity.train_term_task import TrainTermTask
from app.common.extension import session


class TrainTermTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainTermTask).filter(~TrainTermTask.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(TrainTermTask).filter(TrainTermTask.train_term_task_id == _id,
                                                   ~TrainTermTask.is_deleted).one()

    @staticmethod
    def is_empty_table():
        return session.query(TrainTermTask).filter(~TrainTermTask.is_deleted).count() == 0

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_task_id", "doc_term_id", "train_term_status"]
        # Compose query
        q = session.query(TrainTermTask).filter(~TrainTermTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTermTask, key) == val)
        count = q.count()
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return count, q.all()

    def get_by_model_version_and_doc_term_id(self, model_version, doc_term_id):
        q = session.query(TrainTermTask)\
            .join(TrainTask, TrainTask.train_task_id == TrainTermTask.train_task_id)\
            .filter(TrainTask.model_version == model_version,
                    TrainTermTask.doc_term_id == doc_term_id)
        return q.one()

    def create(self, **kwargs) -> TrainTermTask:
        entity = TrainTermTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list) -> [TrainTermTask]:
        entity_list = [TrainTermTask(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(TrainTermTask).filter(TrainTermTask.train_term_task_id == _id).update({TrainTermTask.is_deleted: True})
        session.flush()

    def update(self, _id, **kwargs):
        entity = session.query(TrainTermTask).filter(TrainTermTask.train_term_task_id == _id)
        entity.update(**kwargs)
        session.flush()
        return entity
