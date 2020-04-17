# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:52 下午

from flask_marshmallow import Schema

from app.common.common import StatusEnum
from app.common.patch import fields
from app.schema.doc_type_schema import DocTypeSchema


class MarkJobSchema(Schema):
    mark_job_id = fields.Integer()
    mark_job_name = fields.String()
    mark_job_type = fields.Function(lambda obj: obj.mark_job_type.value)
    assign_mode = fields.Function(lambda obj: obj.assign_mode.value)
    mark_job_state = fields.Function(lambda obj: StatusEnum(obj.mark_job_status).name)
    mark_job_desc = fields.String()
    task_list = fields.List(fields.Integer())
    created_time = fields.DateTime()
    assessor_id = fields.Function(lambda obj: obj.reviewer_ids[0] if len(obj.reviewer_ids) > 0 else 0)

    doc_type = fields.Nested(DocTypeSchema, exclude=('doc_term_list',))
    labeler_ids = fields.List(fields.Integer(), attribute='annotator_ids')
    stats = fields.Nested({
        "all": fields.Integer(),
        "labeled": fields.Integer(),
        "audited": fields.Integer()
    })

