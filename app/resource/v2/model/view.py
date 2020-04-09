# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:29 下午
from typing import Tuple, Dict, Any
from flask_restful import Resource, abort
from app.common.common import NlpTaskEnum, Common, StatusEnum
from app.common.patch import parse, fields
from app.common.filters import CurrentUserMixin
from app.schema.doc_type_schema import DocTypeSchema
from app.schema.evaluate_task_schema import EvaluateTaskSchema
from app.schema.train_job_schema import TrainJobSchema
from app.schema.train_task_schema import TrainTaskSchema
from app.service.doc_type_service import DocTypeService
from app.service.model_service import ModelService


class ModelListResource(Resource, CurrentUserMixin):
    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(missing=0),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取模型记录，分页
        """
        nlp_task_id = Common().get_nlp_task_id_by_route()
        args.update({
            'nlp_task_id': nlp_task_id
        })
        count, train_job_list = ModelService().get_train_job_list_by_nlp_task_id(nlp_task_id=nlp_task_id,
                                                                                 doc_type_id=args['doc_type_id'],
                                                                                 search=args['query'],
                                                                                 offset=args['offset'],
                                                                                 limit=args['limit'],
                                                                                 current_user=self.get_current_user())
        # convert int status to string
        for train_job in train_job_list:
            train_job.train_job_status = StatusEnum(train_job.train_job_status).name
            for train_task in train_job.train_list:
                train_task.train_status = StatusEnum(train_task.train_status).name
        # get the serialized result
        result = TrainJobSchema().dump(train_job_list, many=True)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "model_name": fields.String(required=True),
        "model_desc": fields.String(missing=""),
        "doc_type_id": fields.Integer(required=True),
        "model_train_config": fields.Raw(required=True),  # algorithm_type = ('extract', 'ner', 'seg', 'pos')
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        创建模型
        """
        # create new
        train_job = ModelService().create_train_job_by_doc_type_id(doc_type_id=args["doc_type_id"],
                                                                   train_job_name=args["model_name"],
                                                                   train_job_desc=args["model_desc"],
                                                                   train_config=args["model_train_config"],
                                                                   mark_job_ids=args["mark_job_ids"])

        # convert int status to string
        train_job.train_job_status = StatusEnum(train_job.train_job_status).name
        for train_task in train_job.train_list:
            train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainJobSchema().dump(train_job)
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ClassifyModelListResource(Resource, CurrentUserMixin):
    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(missing=0),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取模型记录，分页
        """
        count, train_job_list = ModelService().get_train_job_list_by_nlp_task_id(nlp_task_id=int(NlpTaskEnum.classify),
                                                                                 doc_type_id=args['doc_type_id'],
                                                                                 search=args['query'],
                                                                                 offset=args['offset'],
                                                                                 limit=args['limit'],
                                                                                 current_user=self.get_current_user())
        # convert int status to string
        for train_job in train_job_list:
            train_job.train_job_status = StatusEnum(train_job.train_job_status).name
            for train_task in train_job.train_list:
                train_task.train_status = StatusEnum(train_task.train_status).name
        # get the serialized result
        result = TrainJobSchema().dump(train_job_list, many=True)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "model_name": fields.String(required=True),
        "model_desc": fields.String(missing=""),
        "doc_type_id": fields.Integer(required=True),
        "model_train_config": fields.Dict(required=True),
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
        "custom_id": fields.Integer(missing=0),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        train_job = ModelService().create_classify_train_job_by_doc_type_id(
            doc_type_id=args["doc_type_id"], train_job_name=args["model_name"], train_job_desc=args["model_desc"],
            train_config=args["model_train_config"], mark_job_ids=args["mark_job_ids"], custom_id=args['custom_id'])
        # convert int status to string
        train_job.train_job_status = StatusEnum(train_job.train_job_status).name
        for train_task in train_job.train_list:
            train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainJobSchema().dump(train_job)
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ModelItemResource(Resource):
    def get(self: Resource, model_id: int) -> Tuple[Dict[str, Any], int]:
        """
        获取单条模型记录
        """
        train_job = ModelService().get_train_job_by_id(model_id)
        # convert int status to string
        train_job.train_job_status = StatusEnum(train_job.train_job_status).name
        for train_task in train_job.train_list:
            train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainJobSchema().dump(train_job)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    def delete(self: Resource, model_id: int) -> Tuple[Dict[str, Any], int]:
        """
        删除单条模型记录
        """
        ModelService().delete_train_job_by_id(model_id)
        return {
                   "message": "删除成功",
               }, 200


class DocTypeInfoListResource(Resource, CurrentUserMixin):
    def get(self):
        nlp_task_id = Common().get_nlp_task_id_by_route()
        result = DocTypeService().get_doc_type_info_by_nlp_task_by_user(nlp_task_id=nlp_task_id,
                                                                        current_user=self.get_current_user())
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200


class DocTypeLatestInfoResource(Resource, CurrentUserMixin):
    @parse({
        "doc_type_id": fields.Integer(required=True)
    })
    def get(self, args):
        """
        查看抽取文档类型下的最新上线模型信息
        """
        data = ModelService().get_latest_model_info_by_doc_type_id(doc_type_id=args["doc_type_id"],
                                                                   current_user=self.get_current_user())
        if not data:
            abort(400, message="未查询到数据")
        # assign
        train_task, evaluate_task, train_job, doc_type = data
        # convert int status to string
        train_task.train_status = StatusEnum(train_task.train_status).name
        train_job.train_job_status = StatusEnum(train_job.train_job_status).name
        evaluate_task.evaluate_task_status = StatusEnum(evaluate_task.evaluate_task_status).name
        result = {
            "doc_type": DocTypeSchema().dump(doc_type),
            "model": TrainJobSchema().dump(train_job),
            "train": TrainTaskSchema().dump(train_task),
            "evaluate": EvaluateTaskSchema().dump(evaluate_task),
        }
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200
