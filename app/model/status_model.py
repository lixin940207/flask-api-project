# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/15
from abc import ABC

from app.model.base import BaseModel
from app.entity.status import Status
from app.common.extension import session


class StatusModel(BaseModel, ABC):
    def get_all(self):
        return session.query(Status).filter(Status.is_deleted==False).all()

    def get_by_id(self, _id):
        return session.query(Status).filter(Status.status_id == _id, not Status.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        pass

    def create(self, entity):
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(Status).filter(Status.status_id == _id).update({Status.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(Status).filter(Status.status_id.in_(_id_list)).update({Status.is_deleted: True})
        session.flush()

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        pass
