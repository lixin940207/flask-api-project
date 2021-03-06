# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:52 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields


class EvaluateTaskSchema(Schema):
    model_evaluate_id = fields.Integer(attribute="evaluate_task_id")
    model_evaluate_name = fields.String(attribute="evaluate_task_name")
    model_evaluate_desc = fields.String(attribute="evaluate_task_desc")
    model_evaluate_state = fields.Function(lambda obj: StatusEnum(obj.evaluate_task_status).name)
    model_evaluate_result = fields.Dict(attribute="evaluate_task_result")
    model_id = fields.Integer(attribute="train_job_id")
    mark_job_ids = fields.List(fields.Integer())
    created_time = fields.DateTime()
    last_updated_time = fields.DateTime(attribute="updated_time")
