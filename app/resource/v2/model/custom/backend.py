# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/8-11:12 上午
from flask_restful import Resource
from typing import Tuple, Dict, Any

from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.service.model_custom_service import ModelCustomService


class UpdateCustomModelResource(Resource):
    @parse({
        "custom_id": fields.Integer(required=True),
        "custom_state": fields.String(required=True, validate=lambda x: x in ['success', 'failed'])
    })
    def post(self: Resource, args) -> Tuple[Dict[str, Any], int]:
        """
        更新自定义模型状态
        """
        update_params = {"custom_algorithm_status": status_str2int_mapper()[args["custom_state"]]}
        ModelCustomService().update_custom_algorithm_by_id(custom_algorithm_id=args["custom_id"], args=update_params)
        return {
                   "message": "更新成功",
               }, 201