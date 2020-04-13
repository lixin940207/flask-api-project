# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:54 下午
from marshmallow import Schema

from app.common.patch import fields
from app.schema import DocTypeSchema, EvaluateTaskSchema, TrainTaskSchema


class TrainJobSchema(Schema):  # type: ignore
    model_id = fields.Integer(attribute='train_job_id')
    model_name = fields.String(attribute="train_job_name")
    model_desc = fields.String(attribute="train_job_desc")
    status = fields.Function(lambda obj: not obj.is_deleted)
    doc_type = fields.Nested(DocTypeSchema)
    created_time = fields.String()
    model_version = fields.String()
    train_list = fields.List(fields.Nested(TrainTaskSchema))
    model_evaluate = fields.Nested(EvaluateTaskSchema)
