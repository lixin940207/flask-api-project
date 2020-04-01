from flask_marshmallow import Schema
from app.common.patch import fields


class GeneralTaskSchema(Schema):
    task_id = fields.Integer()
    task_result = fields.Dict()
    task_state = fields.String(attribute='task_state.value')
    task_type = fields.String(attribute='task_type.value')
    doc = fields.Nested({
        "doc_id": fields.Integer(),
        "doc_raw_name": fields.String(),
        "doc_unique_name": fields.String(),
    })


class ClassifyDocTypeSchema(Schema):
    pass


class ClassifyMarkJobSchema(Schema):  # type: ignore
    doc_type = fields.Nested(ClassifyDocTypeSchema, exclude=('doc_term_list',))
    task_list = fields.List(fields.Nested(GeneralTaskSchema))
    labeler_ids = fields.List(fields.Integer())
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
