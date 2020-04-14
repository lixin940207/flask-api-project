# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:55 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields
from app.schema import UserTaskSchema
from app.schema.doc_schema import DocSchema


class MarkTaskSchema(Schema):  # type: ignore
    task_id = fields.Integer(attribute="mark_task_id")
    mark_job_id = fields.Integer()
    doc_id = fields.Integer()
    doc = fields.Nested(DocSchema)
    doc_type = fields.Nested({
        "doc_type_id": fields.Integer(),
        "doc_type_name": fields.String(),
        "doc_type_desc": fields.String(),
    })
    user_task_list = fields.List(fields.Nested(UserTaskSchema))
    task_state = fields.Function(lambda obj: StatusEnum(obj.mark_task_status).name)
    status = fields.Function(lambda obj: not obj.is_deleted)
    created_time = fields.String()
    task_result = fields.List(fields.Dict, attribute="mark_task_result")
