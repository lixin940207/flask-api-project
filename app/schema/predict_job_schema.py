# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-3:11 下午
from marshmallow import Schema

from app.common.patch import fields
from app.schema.doc_type_schema import DocTypeSchema
from app.schema.predict_task_schema import PredictTaskSchema


class PredictJobSchema(Schema):
    doc_type = fields.Nested(DocTypeSchema)
    task_list = fields.List(fields.Nested(PredictTaskSchema))
    extract_job_id = fields.Integer(attribute="predict_job_id")
    extract_job_name = fields.String(attribute="predict_job_name")
    extract_job_type = fields.String(attribute="predict_job_type.value")
    extract_job_state = fields.String(attribute="predict_job_status")
    extract_job_desc = fields.String(attribute="predict_job_desc")
    is_batch = fields.Boolean()
    created_time = fields.DateTime()