# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_term_model.py 
@Time: 2020/03/18 14:54
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from abc import ABC

from app.model.base import BaseModel
from app.entity.doc_term import DocTerm
from app.common.extension import session
from app.schema.doc_term_schema import DocTermSchema


class DocTermModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocTerm).filter(~DocTerm.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocTerm).filter(DocTerm.doc_term_id == _id, ~DocTerm.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_term_name", "doc_type_id"]
        # Compose query
        q = session.query(DocTerm).filter(~DocTerm.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(DocTerm, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: DocTerm) -> DocTerm:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(DocTerm).filter(DocTerm.doc_term_id == _id).update({DocTerm.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(DocTerm).filter(DocTerm.doc_term_id.in_(_id_list)).update({DocTerm.is_deleted: True})
        session.flush()

    def update(self, entity):
        session.query(DocTerm).update(entity)
        session.flush()

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(DocTerm, entity_list)
        session.flush()

    def get_by_exclude_terms(self, exclude_terms_ids, limit=10, offset=0):
        q = session.query(DocTerm).filter(DocTerm.doc_term_id.notin_(exclude_terms_ids), ~DocTerm.is_deleted)
        count = q.count()
        items = q.offset(offset).limit(limit).all()
        result = DocTermSchema(many=True).dump(items)
        return result, count
