# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/14
from app.common.extension import db
from app.entity.base import BaseEntity


class ClassifyDocRule(BaseEntity):
    classify_rule_id = db.Column(db.Integer(), primary_key=True)
    rule_type = db.Column(db.String(255), nullable=False)
    rule_content = db.Column(db.JSON(), default={})
    doc_term_id = db.Column(db.Integer(), db.ForeignKey("doc_term.doc_term_id"), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
