# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/10
from app.common.extension import db
from app.entity.base import BaseEntity


class WordsegDocLexicon(BaseEntity):
    wordseg_lexicon_id = db.Column(db.Integer(), primary_key=True)
    seg_type = db.Column(db.String(256), nullable=False)  # 词性
    word = db.Column(db.String(512), nullable=False)
    is_active = db.Column(db.Boolean, default=False)  # 启用 禁用
    doc_type_id = db.Column(db.Integer(), db.ForeignKey('doc_type.doc_type_id'), nullable=False)