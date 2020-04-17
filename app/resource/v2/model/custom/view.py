# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-2:57 下午
from flask_restful import Resource, abort
from typing import Dict, Any, Tuple

from app.common.common import StatusEnum, NlpTaskEnum
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema import CustomAlgorithmSchema
from app.service.model_custom_service import ModelCustomService

CUSTOM_MODEL_TYPES = ('extract', 'classify', 'wordseg', 'ner', 'relation')


class CustomListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "custom_types": fields.String(),
        "custom_states": fields.String(),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取自定义容器list，分页，可以根据[custom_types]和[custom_states]过滤
        """
        # get filtered list
        filtered_list = {}
        if args.get("custom_types"):
            nlp_task_id_list = []
            for nlp_task in args.get("custom_types").split(','):
                if nlp_task == 'ner':
                    nlp_task = 'extract'
                nlp_task_id_list.append(int(NlpTaskEnum[nlp_task]))
            filtered_list.update(nlp_task_id_list=nlp_task_id_list)
        if args.get("custom_states"):
            filtered_list.update(custom_algorithm_status_list=[status_str2int_mapper().get(status, int(StatusEnum[status])) for status in args['custom_states'].split(',')])
        count, custom_algorithm_list = ModelCustomService().get_custom_algorithm_list_by_filter_in(offset=args["offset"], limit=args["limit"], args=filtered_list)
        result = CustomAlgorithmSchema(many=True).dump(custom_algorithm_list)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        'custom_ip': fields.String(required=True),
        'custom_port': fields.Integer(required=True),
        'custom_evaluate_port': fields.Integer(required=True),
        'custom_name': fields.String(required=True),
        'custom_id_name': fields.String(required=True),
        'custom_desc': fields.String(missing=""),
        'custom_config': fields.String(missing={}),
        'custom_type': fields.String(required=True, validate=lambda x: x in CUSTOM_MODEL_TYPES),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:

        # check if unique name exists
        exist_custom_algorithm = ModelCustomService().get_custom_algorithm_by_alias(custom_algorithm_alias=args["custom_id_name"])
        if exist_custom_algorithm:
            abort(400, message="该标识名称已被占用")
        # define preprocess type
        if args["custom_type"] in "ner":
            preprocess_type = {"split_by_sentence": True}
            args.update(custom_type="extract")
        elif args["custom_type"] == "wordseg":
            preprocess_type = {"split_by_sentence": True}
        elif args["custom_type"] == "realation":
            preprocess_type = {}
        else: # wordseg
            preprocess_type = {"split_by_sentence": False}
        # create new
        custom_algorithm = ModelCustomService().create_custom_algorithm(custom_algorithm_alias=args["custom_id_name"],
                                                                        custom_algorithm_name=args["custom_name"],
                                                                        custom_algorithm_desc=args["custom_desc"],
                                                                        custom_algorithm_ip=args["custom_ip"],
                                                                        custom_algorithm_predict_port=args["custom_port"],
                                                                        custom_algorithm_evaluate_port=args["custom_evaluate_port"],
                                                                        custom_algorithm_config=args["custom_config"],
                                                                        preprocess=preprocess_type,
                                                                        nlp_task_id=int(NlpTaskEnum[args["custom_type"]]))
        result = CustomAlgorithmSchema().dump(custom_algorithm)

        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class CustomItemResource(Resource):
    def get(self: Resource, custom_id: int) -> Tuple[Dict[str, Any], int]:
        """
        获取单条自定义容器的记录
        """
        custom_algorithm = ModelCustomService().get_custom_algorithm_by_id(custom_algorithm_id=custom_id)
        result = CustomAlgorithmSchema().dump(custom_algorithm)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        'custom_ip': fields.String(required=True),
        'custom_port': fields.Integer(required=True),
        'custom_evaluate_port': fields.Integer(required=True),
        'custom_name': fields.String(required=True),
        'custom_desc': fields.String(allow_none=True),
        'custom_config': fields.String(allow_none=True),
    })
    def put(self: Resource, args, custom_id: int) -> Tuple[Dict[str, Any], int]:
        # generate update params
        update_params = {"custom_algorithm_ip": args["custom_ip"],
                         "custom_algorithm_predict_port": args["custom_port"],
                         "custom_algorithm_evaluate_port": args["custom_evaluate_port"],
                         "custom_algorithm_name": args["custom_name"]}
        if args.get("custom_desc"):
            update_params.update(custom_algorithm_desc=args["custom_desc"])
        if args.get("custom_config"):
            update_params.update(custom_algorithm_config=args["custom_config"])
        custom_algorithm = ModelCustomService().update_custom_algorithm_by_id(custom_algorithm_id=custom_id, args=update_params)
        result = CustomAlgorithmSchema().dump(custom_algorithm)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    def delete(self: Resource, custom_id: int) -> Tuple[Dict[str, Any], int]:
        ModelCustomService().delete_custom_algorithm_by_id(custom_algorithm_id=custom_id)
        return {
                   "message": "删除成功"
               }, 200


class CheckCustomIdNameResource(Resource):
    @parse({
        'custom_id_name': fields.String(required=True),
        'custom_type': fields.String(required=True, validate=lambda x: x in CUSTOM_MODEL_TYPES),
    })
    def get(self: Resource, args) -> Tuple[Dict[str, Any], int]:
        """
        检查唯一标识名是否已经存在
        """
        exist_custom_algorithm = ModelCustomService().get_custom_algorithm_by_alias(custom_algorithm_alias=args["custom_id_name"])
        if exist_custom_algorithm:
            result = dict(available=False, tip='该名称已被占用')
        else:
            result = dict(available=True, tip='可以使用')
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200


class CustomModelExportResource(Resource):
    def post(self: Resource, custom_id) -> Tuple[Dict[str, Any], int]:
        """
        导出
        """
        result = ModelCustomService().export_custom_algorithm_by_id(custom_algorithm_id=custom_id)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200