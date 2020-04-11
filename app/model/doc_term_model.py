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
from app.entity import DocTerm, DocType
from app.common.extension import session


class DocTermModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocTerm).filter(~DocTerm.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocTerm).filter(DocTerm.doc_term_id == _id, ~DocTerm.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_term_name", "doc_type_id"]
        # Compose query
        q = session.query(DocTerm).filter(~DocTerm.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(DocTerm, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(DocTerm, order_by).desc())
        else:
            q = q.order_by(getattr(DocTerm, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> DocTerm:
        entity = DocTerm(**kwargs)
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
        session.merge([DocTerm(**e) for e in entity_list])
        session.flush()

    @staticmethod
    def get_by_exclude_terms(exclude_terms_ids, limit=10, offset=0):
        q = session.query(DocTerm).filter(DocTerm.doc_term_id.notin_(exclude_terms_ids), ~DocTerm.is_deleted)
        count = q.count()
        items = q.offset(offset).limit(limit).all()
        return items, count

    @staticmethod
    def get_doc_term_by_doctype(doc_type_id, offset=0, limit=10, doc_term_ids=None):
        q = session.query(DocTerm).join(DocType, DocType.doc_type_id == DocTerm.doc_type_id).\
            filter(DocTerm.doc_type_id == doc_type_id, ~DocTerm.is_deleted, ~DocType.is_deleted)
        if doc_term_ids:
            q = q.filter(DocTerm.doc_term_id.in_(doc_term_ids))
        count = q.count()
        items = q.offset(offset).limit(limit).all()
        return items, count
