# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: relation_m2m_term_model.py 
@Time: 2020/03/18 14:57
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from abc import ABC

from sqlalchemy import func
from app.entity import DocTerm, DocRelation
from app.model.base import BaseModel
from app.entity.relation_m2m_term import RelationM2mTerm
from app.common.extension import session


class RelationM2mTermModel(BaseModel, ABC):
    def get_all(self):
        return session.query(RelationM2mTerm).filter(RelationM2mTerm.is_deleted == False).all()

    def get_by_id(self, _id):
        return session.query(RelationM2mTerm).filter(RelationM2mTerm.id == _id, not RelationM2mTerm.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_relation_id", "doc_term_id"]
        # Compose query
        q = session.query(RelationM2mTerm).filter(RelationM2mTerm.is_deleted == False)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(RelationM2mTerm, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: RelationM2mTerm) -> RelationM2mTerm:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(RelationM2mTerm).filter(RelationM2mTerm.id == _id).update({RelationM2mTerm.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(RelationM2mTerm).filter(RelationM2mTerm.id.in_(_id_list)).update({RelationM2mTerm.is_deleted: True})
        session.flush()

    def update(self, entity):
        session.query(RelationM2mTerm).update(entity)
        session.flush()

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(RelationM2mTerm, entity_list)
        session.flush()

    @staticmethod
    def get_relation_term_mapping(doc_type_id):
        q = session.query(RelationM2mTerm.doc_relation_id,
                      func.group_concat(RelationM2mTerm.doc_term_id.distinct()))\
            .join(DocTerm, DocTerm.doc_term_id, RelationM2mTerm.doc_relation_id)\
            .join(DocRelation, DocRelation.doc_relation_id, RelationM2mTerm.doc_relation_id)\
            .filter(~DocTerm.is_deleted, ~DocRelation.is_deleted, ~RelationM2mTerm.is_deleted,
                    DocTerm.doc_type_id == doc_type_id)\
            .group_by(RelationM2mTerm.doc_relation_id)
        return q.all()
