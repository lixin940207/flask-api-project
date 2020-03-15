# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
from abc import ABC

from app.model.base import BaseModel
from app.entity.nlp_task import NlpTask
from app.common.extension import session


class NlpTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(NlpTask).filter(NlpTask.is_deleted==False).all()

    def get_by_id(self, _id):
        return session.query(NlpTask).filter(NlpTask.nlp_task_id == _id, not NlpTask.is_deleted).one()

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
        session.query(NlpTask).filter(NlpTask.nlp_task_id == _id).update({NlpTask.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(NlpTask).filter(NlpTask.nlp_task_id.in_(_id_list)).update({NlpTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(NlpTask, entity_list)
        session.flush()
