# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:52 下午

from flask_marshmallow import Schema
from app.common.patch import fields
from app.schema.doc_type_schema import DocTypeSchema


class MarkJobSchema(Schema):
    doc_type = fields.Nested(DocTypeSchema, exclude=('doc_term_list',))
    labeler_ids = fields.List(fields.Integer(), attribute='annotator_ids')
    stats = fields.Nested({
        "all": fields.Integer(),
        "labeled": fields.Integer(),
        "audited": fields.Integer()
    })

    class Meta:
        fields = (
            'mark_job_id',
            'mark_job_name',
            'mark_job_type',
            'assign_mode',
            'mark_job_state',
            'mark_job_desc',
            "doc_type",
            "task_list",
            'stats',
            'labeler_ids',
            'assessor_id',
            'created_time'
        )
