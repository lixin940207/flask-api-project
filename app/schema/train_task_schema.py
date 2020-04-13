# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:54 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields
from app.schema.train_term_task_schema import TrainTermTaskSchema


class TrainTaskSchema(Schema):  # type: ignore
    model_train_id = fields.Integer(attribute="train_task_id")
    model_train_config = fields.Dict(attribute="train_config")
    model_train_state = fields.Function(lambda obj: StatusEnum(obj.train_status).name)
    model_id = fields.Integer(attribute="train_job_id")
    mark_job_ids = fields.List(fields.Integer())
    train_terms = fields.List(fields.Nested(TrainTermTaskSchema))
    created_time = fields.DateTime()
    last_updated_time = fields.DateTime(attribute="updated_time")
