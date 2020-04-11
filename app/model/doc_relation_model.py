# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_relation_model.py 
@Time: 2020/03/18 14:52
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from abc import ABC

from app.model.base import BaseModel
from app.entity import DocRelation
from app.common.extension import session


class DocRelationModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocRelation).filter(DocRelation.is_deleted == False).all()

    def get_by_id(self, _id):
        return session.query(DocRelation).filter(DocRelation.doc_relation_id == _id, not DocRelation.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_relation_name", "doc_type_id"]
        # Compose query
        q = session.query(DocRelation).filter(DocRelation.is_deleted == False)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(DocRelation, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: DocRelation) -> DocRelation:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(DocRelation).filter(DocRelation.doc_relation_id == _id).update({DocRelation.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(DocRelation).filter(DocRelation.custom_algorithm_id.in_(_id_list)).update(
            {DocRelation.is_deleted: True})
        session.flush()

    def update(self, entity):
        session.query(DocRelation).update(entity)
        session.flush()

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(DocRelation, entity_list)
        session.flush()
