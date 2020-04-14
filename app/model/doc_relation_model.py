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
from app.entity import DocRelation, RelationM2mTerm
from app.common.extension import session
from sqlalchemy import func


class DocRelationModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocRelation).filter(~DocRelation.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocRelation).filter(DocRelation.doc_relation_id == _id, ~DocRelation.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, require_count=False, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_relation_ids", "doc_relation_name", "doc_type_id"]
        # Compose query
        q = session.query(DocRelation).filter(~DocRelation.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key == "doc_relation_ids":
                q = q.filter(DocRelation.doc_relation_id.in_(val))
            elif key in accept_keys:
                q = q.filter(getattr(DocRelation, key) == val)
        count = 0
        if require_count:
            count = q.count()
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(DocRelation, order_by).desc())
        else:
            q = q.order_by(getattr(DocRelation, order_by))
        q = q.offset(offset).limit(limit)
        return q.all(), count

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

    @staticmethod
    def get_relation_with_terms(order_by="created_time", order_by_desc=True, limit=10, offset=0, require_count=False,
                                **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_relation_name", "doc_type_id"]
        # Compose query
        q = session.query(DocRelation.doc_relation_id, DocRelation.doc_relation_name, DocRelation.created_time,
                          func.group_concat(RelationM2mTerm.doc_term_id.distinct()))\
            .join(RelationM2mTerm, RelationM2mTerm.doc_relation_id == DocRelation.doc_relation_id)\
            .filter(~DocRelation.is_deleted, ~RelationM2mTerm.is_deleted)\

        # Filter conditions
        for key, val in kwargs.items():
            if key == "doc_relation_ids" and len(val) > 0:
                q = q.filter(DocRelation.doc_relation_id.in_(val))
            elif key in accept_keys:
                q = q.filter(getattr(DocRelation, key) == val)
        q = q.group_by(RelationM2mTerm.doc_relation_id, DocRelation.doc_relation_name, DocRelation.created_time)
        count = 0
        if require_count:
            count = q.count()
        # Order by key
        if order_by == "order_by" and order_by_desc:
            q = q.order_by(DocRelation.created_time.desc())
        q = q.offset(offset).limit(limit)
        return q.all(), count
