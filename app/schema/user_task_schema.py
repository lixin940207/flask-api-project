# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:55 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields
from app.schema.doc_schema import DocSchema


class UserTaskSchema(Schema):  # type: ignore
    doc = fields.Nested(DocSchema)
    doc_type = fields.Nested({
        "doc_type_id": fields.Integer(),
        "doc_type_name": fields.String(),
        "doc_type_desc": fields.String(),
    })
    task_id = fields.Integer(attribute="user_task_id")
    labeler_id = fields.Integer(attribute="annotator_id")
    manual_task_id = fields.Integer(attribute="mark_task_id")
    task_result = fields.List(fields.Dict, attribute="user_task_result")
    task_state = fields.Function(lambda obj: StatusEnum(obj.user_task_status).name)
    status = fields.Function(lambda obj: not obj.is_deleted)
    created_time = fields.String()

