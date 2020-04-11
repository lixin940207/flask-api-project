# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:51 下午
from flask_marshmallow import Schema
from app.common.patch import fields
from app.schema.doc_term_schema import DocTermSchema, WordsegDocLexiconSchema


class DocTypeSchema(Schema):
    doc_type_id = fields.Integer()
    doc_type_name = fields.String()
    doc_type_desc = fields.String()
    is_top = fields.Boolean(attribute="is_favorite")
    created_time = fields.DateTime()
    doc_term_list = fields.List(fields.Nested(DocTermSchema))
    group_id = fields.Integer()
    status = fields.Integer(attribute="is_deleted")


class EntityDocRelationSchema(Schema):
    doc_relation_id = fields.Integer()
    doc_relation_name = fields.String()
    doc_relation_desc = fields.String()
    doc_term_ids = fields.List(fields.Integer())


class EntityDocTypeSchema(Schema):
    doc_term_list = fields.List(fields.Nested(DocTermSchema))
    doc_relation_list = fields.List(fields.Nested(EntityDocRelationSchema))

    doc_type_id = fields.Integer()
    doc_type_name = fields.String()
    doc_type_desc = fields.String()
    is_top = fields.Boolean(attribute="is_favorite")
    created_time = fields.DateTime()
    group_id = fields.Integer()
    status = fields.Integer(attribute="is_deleted")


class WordsegDocTypeSchema(Schema):
    doc_lexicon_list = fields.List(fields.Nested(WordsegDocLexiconSchema), attribute='doc_rules')

    doc_type_id = fields.Integer()
    doc_type_name = fields.String()
    doc_type_desc = fields.String()
    is_top = fields.Boolean(attribute="is_favorite")
    created_time = fields.DateTime()
    doc_term_list = fields.List(fields.Nested(DocTermSchema))
    group_id = fields.Integer()
    status = fields.Integer(attribute="is_deleted")