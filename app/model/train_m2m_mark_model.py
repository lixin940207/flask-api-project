# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/30-5:47 下午
from abc import ABC
from app.entity import TrainM2mMark
from app.model.base import BaseModel
from app.common.extension import session


class TrainM2mMarkbModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainM2mMark).filter(~TrainM2mMark.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(TrainM2mMark).filter(TrainM2mMark.id == _id, ~TrainM2mMark.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_id", "mark_job_id"]
        # Compose query
        q = session.query(TrainM2mMark).filter(~TrainM2mMark.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainM2mMark, key) == val)
        # Order by key, Descending or ascending order
        if order_by_desc:
            q = q.order_by(getattr(TrainM2mMark, order_by).desc())
        else:
            q = q.order_by(getattr(TrainM2mMark, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> TrainM2mMark:
        entity = TrainM2mMark(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list) -> [TrainM2mMark]:
        entity_list = [TrainM2mMark(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(TrainM2mMark).filter(TrainM2mMark.id == _id).update({TrainM2mMark.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mapping
        pass