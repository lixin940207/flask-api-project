# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/15
from abc import ABC

from app.common.extension import session
from app.entity import ClassifyDocRule, DocTerm, DocType
from app.model.base import BaseModel


class ClassifyRuleModel(BaseModel, ABC):
    def get_all(self):
        pass

    def get_by_id(self, _id):
        session.query(ClassifyDocRule).filter(ClassifyDocRule.classify_rule_id == _id, ~ClassifyDocRule.is_deleted).one()

    def get_by_filter(self, search, order_by="created_time", order_by_desc=True, limit=10, offset=0,
                      require_count=False, **kwargs):
        pass

    def create(self, **kwargs) -> ClassifyDocRule:
        entity = ClassifyDocRule(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        entity_list = [ClassifyDocRule(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(ClassifyDocRule).filter(ClassifyDocRule.classify_rule_id == _id)\
            .update({ClassifyDocRule.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        pass

    def bulk_delete_by_filter(self, **kwargs):
        pass

    def update(self, doc_rule_id, **kwargs):
        accept_keys = ["rule_content", "state"]
        classify_rule = session.query(ClassifyDocRule).filter(ClassifyDocRule.doc_rule_id == doc_rule_id).one()
        for key, val in kwargs.items():
            if key == "state":
                classify_rule.is_deleted = val
            elif key in accept_keys:
                setattr(classify_rule, key, val)
        session.commit()

        return classify_rule

    def bulk_update(self, entity_list):
        pass

    @staticmethod
    def get_rule_with_term(doc_type_id):
        return session.query(ClassifyDocRule, DocTerm).join(
            DocTerm, DocTerm.doc_term_id == ClassifyDocRule.doc_term_id
        ).join(
            DocType, DocType.doc_type_id == DocTerm.doc_type_id
        ).filter(
            DocType.doc_type_id == doc_type_id,
            ~DocType.is_deleted,
            ~DocTerm.is_deleted,
            ~ClassifyDocRule.is_deleted,
            ClassifyDocRule.is_active
        ).all()
