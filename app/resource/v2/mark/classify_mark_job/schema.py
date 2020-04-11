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


class ClassifyDocTermSchema(Schema):

    class Meta:
        fields = (
            "doc_term_id",
            "doc_term_name",
            "doc_term_color",
            "doc_term_index",
            "doc_term_desc"
        )


class ClassifyDocTypeSchema(Schema):
    doc_term_list = fields.List(fields.Nested(ClassifyDocTermSchema), attribute='doc_terms')

    class Meta:
        fields = (
            'doc_type_id',
            'doc_type_name',
            'doc_type_desc',
            'doc_term_list',
            'created_time',
            'status',
            'index',
            'is_top',
        )


class ClassifyMarkJobSchema(Schema):
    doc_type = fields.Nested(ClassifyDocTypeSchema, exclude=('doc_term_list',))
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
