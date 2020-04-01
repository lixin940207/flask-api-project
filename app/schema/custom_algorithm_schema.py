# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:50 下午
from flask_marshmallow import Schema
from app.common.patch import fields


class CustomAlgorithmSchema(Schema):
    custom_id = fields.Integer(attribute="custom_algorithm_id")
    custom_ip = fields.String(attribute="custom_algorithm_ip")
    custom_port = fields.Integer(attribute="custom_algorithm_predict_port")
    custom_evaluate_port = fields.Integer(attribute="custom_algorithm_evaluate_port")
    custom_name = fields.String(attribute="custom_algorithm_name")
    custom_id_name = fields.String(attribute="custom_algorithm_alias")
    custom_desc = fields.String(attribute="custom_algorithm_desc")
    custom_type = fields.String(attribute="nlp_task")
    custom_state = fields.String(attribute="custom_algorithm_status")
    custom_config = fields.String(attribute="custom_algorithm_config")
    created_time = fields.DateTime()
