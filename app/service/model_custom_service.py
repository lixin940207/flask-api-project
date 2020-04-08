# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/8-11:16 上午
import json

import requests
from flask_restful import abort

from app.common.common import StatusEnum
from app.common.extension import session
from app.entity import CustomAlgorithm
from app.model.custom_algorithm_model import CustomAlgorithmModel


class ModelCustomService:
    @staticmethod
    def get_custom_algorithm_by_id(custom_algorithm_id) -> CustomAlgorithm:
        custom_algorithm = CustomAlgorithmModel().get_by_id(custom_algorithm_id)
        return custom_algorithm

    @staticmethod
    def get_custom_algorithm_by_alias(custom_algorithm_alias) -> CustomAlgorithm:
        custom_algorithm = CustomAlgorithmModel().get_by_filter(custom_algorithm_alias=custom_algorithm_alias)
        return custom_algorithm

    @staticmethod
    def get_custom_algorithm_list_by_filter_in(offset, limit, args) -> (int, [CustomAlgorithm]):
        count, custom_algorithm_list = CustomAlgorithmModel().get_by_filter_in(offset=offset, limit=limit, **args)
        return count, custom_algorithm_list

    @staticmethod
    def create_custom_algorithm(**kwargs) -> CustomAlgorithm:
        custom_algorithm = CustomAlgorithmModel().create(custom_algorithm_status=int(StatusEnum.available), **kwargs)
        session.commit()
        return custom_algorithm

    @staticmethod
    def update_custom_algorithm_by_id(custom_algorithm_id, args) -> CustomAlgorithm:
        custom_algorithm = CustomAlgorithmModel().update(custom_algorithm_id, **args)
        session.commit()
        return custom_algorithm

    @staticmethod
    def delete_custom_algorithm_by_id(custom_algorithm_id):
        CustomAlgorithmModel().delete(custom_algorithm_id)
        session.commit()

    @staticmethod
    def export_custom_algorithm_by_id(custom_algorithm_id):
        custom_algorithm = CustomAlgorithmModel().get_by_id(custom_algorithm_id)
        if not custom_algorithm:
            abort(400, message="该自定义模型不存在")
        resp = requests.post(f'http://{custom_algorithm.custom_algorithm_ip}:{custom_algorithm.custom_algorithm_predict_port}/docker', json={
            "custom_algorithm_id": custom_algorithm.custom_algorithm_id,
            "al_name": custom_algorithm.custom_algorithm_alias
        })
        result = json.loads(resp.text)
        if result['status'] == 'FAIL':
            abort(500, message=f"导出服务 <{custom_algorithm.custom_algorithm_ip}:{custom_algorithm.custom_algorithm_predict_port}> 出现错误")

        CustomAlgorithmModel().update(custom_algorithm_id, export_url=result['image_name'], custom_state=int(StatusEnum.processing))
        session.commit()
        return result
