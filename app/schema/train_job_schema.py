# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:54 下午
from marshmallow import Schema
from app.common.patch import fields
from app.schema.doc_type_schema import DocTypeSchema
from app.schema.evaluate_task_schema import EvaluateTaskSchema
from app.schema.train_task_schema import TrainTaskSchema


class TrainJobSchema(Schema):  # type: ignore
    model_id = fields.Integer(attribute='train_job_id')
    model_name = fields.String(attribute="train_job_name")
    model_desc = fields.String(attribute="train_job_desc")
    status = fields.Integer(attribute='train_job_status')
    doc_type = fields.Nested(DocTypeSchema)
    created_time = fields.String()
    model_version = fields.String()
    train_list = fields.List(fields.Nested(TrainTaskSchema))
    model_evaluate = fields.Nested(EvaluateTaskSchema)
