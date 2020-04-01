from abc import ABC

from sqlalchemy import not_

from app.model.base import BaseModel
from app.entity.doc import Doc
from app.common.extension import session


class DocModel(BaseModel, ABC):
    def get_all(self):
        raise NotImplemented("no get_all")

    @staticmethod
    def is_empty_table():
        return session.query(Doc).filter(not_(Doc.is_deleted)).count() == 0

    def get_by_id(self, _id):
        return session.query(Doc).filter(Doc.doc_id == _id, not_(Doc.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        raise NotImplemented("no get_by_filter")

    def create(self, entity):
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(Doc).filter(Doc.doc_id == _id).update({Doc.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(Doc).filter(Doc.doc_id.in_(_id_list)).update({Doc.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        raise NotImplemented("no bulk_update")
