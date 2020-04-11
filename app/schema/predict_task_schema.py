# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-3:28 下午
from marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields
from app.schema.doc_schema import DocSchema


class PredictTaskSchema(Schema):
    task_id = fields.Integer(attribute="predict_task_id")
    task_result = fields.Dict(attribute="predict_task_result")
    task_state = fields.Function(lambda obj: StatusEnum(obj.predict_task_status).name)
    created_time = fields.DateTime()
    doc = fields.Nested(DocSchema)
