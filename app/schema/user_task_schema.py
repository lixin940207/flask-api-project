# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:55 下午
from flask_marshmallow import Schema

from app.common.patch import fields
from app.schema.doc_schema import DocSchema


class UserTaskSchema(Schema):
    doc = fields.Nested(DocSchema)
    doc_type = fields.Nested({
        "doc_type_id": fields.Integer(),
        "doc_type_name": fields.String(),
        "doc_type_desc": fields.String(),
    })
    row_content = fields.String()

    class Meta:
        fields = (
            'annotator_id',
            'user_task_id',
            'manual_task_id',
            'user_task_status',
            'user_task_result',
            'doc',
            'doc_type',
            'created_time',
            'status',
            'row_content',
        )
