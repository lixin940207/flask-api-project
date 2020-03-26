# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
from abc import ABC

from app.model.base import BaseModel
from app.entity.doc_type import DocType
from app.common.extension import session
from sqlalchemy import func


class DocTypeModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocType).filter(~DocType.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, ~DocType.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_type_name", "nlp_task_id"]
        # Compose query
        q = session.query(DocType).filter(~DocType.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(DocType, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: DocType) -> DocType:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(DocType).filter(DocType.doc_type_id == _id).update({DocType.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(DocType).filter(DocType.doc_type_id.in_(_id_list)).update({DocType.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(DocType, entity_list)

    @staticmethod
    def count_doc_type_by_nlp_task_manager(user_id):
        count = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)).filter(~DocType.is_deleted,
                                                                                           DocType.created_by == user_id) \
            .group_by(DocType.nlp_task_id).all()
        return count
