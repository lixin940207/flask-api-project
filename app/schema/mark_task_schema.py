# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:53 下午
from flask_marshmallow import Schema

from app.common.patch import fields
from app.schema.doc_schema import DocSchema
from app.schema.user_task_schema import UserTaskSchema


class MarkTaskSchema(Schema):
    doc = fields.Nested(DocSchema)
    doc_type = fields.Nested({
        "doc_type_id": fields.Integer(),
        "doc_type_name": fields.String(),
        "doc_type_desc": fields.String(),
    })
    user_task_list = fields.List(fields.Nested(UserTaskSchema))
    row_content = fields.String()

    class Meta:
        fields = (
            'task_id',
            'task_state',
            'task_result',
            'doc',
            'doc_type',
            'created_time',
            'status',
            'doc_type_table',
            'relate_machine_task',
            'machine_task_id',
            'doc_row_id',
            'user_task_list',
            'row_content',
        )
