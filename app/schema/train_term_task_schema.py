# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:54 下午
from flask_marshmallow import Schema
from app.common.patch import fields


class TrainTermTaskSchema(Schema):  # type: ignore
    train_term_id = fields.Integer(attribute="train_term_task_id")
    train_term_result = fields.Dict()
    train_term_state = fields.Integer(attribute="train_term_status")
    model_train_id = fields.Integer(attribute="train_task_id")
    doc_term_id = fields.Integer()