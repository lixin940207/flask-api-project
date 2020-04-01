# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:51 下午
from flask_marshmallow import Schema
from app.common.patch import fields
from app.schema.doc_term_schema import DocTermSchema


class DocTypeSchema(Schema):
    doc_type_id = fields.Integer()
    doc_type_name = fields.String()
    doc_type_desc = fields.String()
    is_top = fields.Boolean(attribute="is_favorite")
    created_time = fields.DateTime()
    doc_term_list = fields.List(fields.Nested(DocTermSchema))
    group_id = fields.Integer()