# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: custom_algorithm_model.py 
@Time: 2020/03/18 14:31
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from abc import ABC

from app.model.base import BaseModel
from app.entity.custom_algorithm import CustomAlgorithm
from app.common.extension import session


class CustomAlgorithmModel(BaseModel, ABC):
    def get_all(self):
        return session.query(CustomAlgorithm).filter(~CustomAlgorithm.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(CustomAlgorithm).filter(CustomAlgorithm.custom_algorithm_id == _id,
                                                     ~CustomAlgorithm.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["custom_algorithm_name", "nlp_task_id"]
        # Compose query
        q = session.query(CustomAlgorithm).filter(~CustomAlgorithm.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(CustomAlgorithm, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> CustomAlgorithm:
        entity = CustomAlgorithm(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(CustomAlgorithm).filter(CustomAlgorithm.custom_algorithm_id == _id).update(
            {CustomAlgorithm.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(CustomAlgorithm).filter(CustomAlgorithm.custom_algorithm_id.in_(_id_list)).update(
            {CustomAlgorithm.is_deleted: True})
        session.flush()

    def update(self, entity):
        session.query(CustomAlgorithm).update(entity)
        session.flush()

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(CustomAlgorithm, entity_list)
        session.flush()
