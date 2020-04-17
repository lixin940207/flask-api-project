# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:50 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields


class DocSchema(Schema):  # type: ignore
    doc_id = fields.Integer()
    doc_unique_name = fields.String()
    doc_raw_name = fields.String()
    convert_state = fields.Function(lambda obj: StatusEnum(obj.doc_status).name)
