# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:52 下午
from flask_marshmallow import Schema

from app.common.common import StatusEnum, NlpTaskEnum
from app.common.patch import fields


class ExportJobSchema(Schema):
    export_id = fields.Integer(attribute="export_job_id")
    file_path = fields.String(attribute="export_file_path")
    mark_type = fields.Function(lambda obj: NlpTaskEnum(obj.nlp_task_id).name)  # nlp_task_id
    export_state = fields.Function(lambda obj: StatusEnum(obj.export_job_status).name)
    project_name = fields.String(attribute="doc_type_name")
    created_time = fields.String()
    mark_job_ids = fields.List(fields.Integer(), attribute="export_mark_job_ids")
