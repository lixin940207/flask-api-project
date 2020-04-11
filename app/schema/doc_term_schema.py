# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:51 下午
from flask_marshmallow import Schema
from app.common.patch import fields


class WordsegDocLexiconSchema(Schema):
    id = fields.Integer(attribute="wordseg_lexicon_id")
    seg_type = fields.String()
    word = fields.String()
    doc_type_id = fields.Integer()
    state = fields.String(attribute="is_active")


class DocTermSchema(Schema):
    doc_term_id = fields.Integer()
    doc_term_name = fields.String()
    doc_term_alias = fields.String()
    # doc_term_index = fields.String()
    doc_term_color = fields.String()
    doc_term_desc = fields.String()
    doc_term_data_type = fields.String()
    doc_term_shortcut = fields.String()


class WordsegDocTermSchema(Schema):
    doc_lexicon_list = fields.List(fields.Nested(WordsegDocLexiconSchema), attribute='doc_rules')

    doc_term_id = fields.Integer()
    doc_term_name = fields.String()
    doc_term_alias = fields.String()
    # doc_term_index = fields.String()
    doc_term_color = fields.String()
    doc_term_desc = fields.String()
    doc_term_data_type = fields.String()
    doc_term_shortcut = fields.String()


class EntityDocTermSchema(Schema):  # type: ignore
    doc_term_id = fields.Integer()
    doc_term_name = fields.String()
    doc_term_alias = fields.String()
    # doc_term_index = fields.String()
    doc_term_color = fields.String()
    doc_term_desc = fields.String()
    doc_term_data_type = fields.String()
    doc_term_shortcut = fields.String()
