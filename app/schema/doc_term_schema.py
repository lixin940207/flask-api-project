# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:51 下午
from flask_marshmallow import Schema
from app.common.patch import fields


class DocTermSchema(Schema):  # type: ignore
    doc_term_id = fields.Integer()
    doc_term_name = fields.String()
    doc_term_alias = fields.String()
    doc_term_index = fields.String(attribute="doc_term_shortcut")
    doc_term_color = fields.String()
    doc_term_desc = fields.String()
    doc_term_data_type = fields.String()
