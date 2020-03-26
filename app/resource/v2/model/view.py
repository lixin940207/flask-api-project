# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:29 下午
from typing import Tuple, Dict, Any
from flask_restful import Resource, abort
from app.common.patch import parse, fields
from app.common.filters import QueryByRoleMixin
from app.service.model_service import ModelService


class ModelListResource(Resource, QueryByRoleMixin):
    # def filter_by_admin(self, q, params):
    #     return q.join(DocType, DocType.doc_type_id == Model.doc_type_id) \
    #         .filter(DocType.status, DocType.creator_id == g.user_id)

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
        user_role = self.get_current_role()
        if args.get("doc_type_id"):  # 获取某个doc_type项目的模型列表
            count, result = ModelService().get_train_job_list_by_doc_type_id(
                doc_type_id=args['doc_type_id'], search=args['query'], offset=args['offset'], limit=args['limit'])
        else:  # 获取全部的模型列表
            count, result = ModelService().get_train_job_list_by_nlp_task(
                nlp_task='extract', search=args['query'], offset=args['offset'], limit=args['limit'])
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
        result = ModelService().create_train_job_by_doc_type_id(
            doc_type_id=args["doc_type_id"], train_job_name=args["model_name"], train_job_desc=args["model_desc"],
            train_config=args["model_train_config"], mark_job_ids=args["mark_job_ids"])
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ClassifyModelListResource(Resource, QueryByRoleMixin):
    # def filter_by_admin(self, q, params):
    #     return q.join(DocType, DocType.doc_type_id == Model.doc_type_id) \
    #         .filter(DocType.status, DocType.creator_id == g.user_id)

    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取模型记录，分页
        """
        user_role = self.get_current_role()
        if args.get("doc_type_id"):  # 获取某个doc_type项目的模型列表
            count, result = ModelService().get_train_job_list_by_doc_type_id(
                doc_type_id=args['doc_type_id'], search=args['query'], offset=args['offset'], limit=args['limit'])
        else:  # 获取全部的模型列表
            count, result = ModelService().get_train_job_list_by_nlp_task(
                nlp_task='classify', search=args['query'], offset=args['offset'], limit=args['limit'])
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
        result = ModelService().create_classify_train_job_by_doc_type_id(
            doc_type_id=args["doc_type_id"], train_job_name=args["model_name"], train_job_desc=args["model_desc"],
            train_config=args["model_train_config"], mark_job_ids=args["mark_job_ids"], custom_id=args['custom_id'])
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class RelationModelListResource(Resource, QueryByRoleMixin):
    # def filter_by_admin(self, q, params):
    #     return q.join(DocType, DocType.doc_type_id == Model.doc_type_id) \
    #         .filter(DocType.status, DocType.creator_id == g.user_id)
    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取模型记录，分页
        """
        user_role = self.get_current_role()
        if args.get("doc_type_id"):  # 获取某个doc_type项目的模型列表
            count, result = ModelService().get_train_job_list_by_doc_type_id(
                doc_type_id=args['doc_type_id'], search=args['query'], offset=args['offset'], limit=args['limit'])
        else:  # 获取全部的模型列表
            count, result = ModelService().get_train_job_list_by_nlp_task(
                nlp_task='relation', search=args['query'], offset=args['offset'], limit=args['limit'])
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "model_name": fields.String(required=True),
        "model_desc": fields.String(missing=""),
        "doc_type_id": fields.Integer(required=True),
        "model_train_config": fields.Raw(required=True),
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        创建模型
        """
        result = ModelService().create_train_job_by_doc_type_id(
            doc_type_id=args["doc_type_id"], train_job_name=args["model_name"], train_job_desc=args["model_desc"],
            train_config=args["model_train_config"], mark_job_ids=args["mark_job_ids"])
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class WordsegModelListResource(Resource, QueryByRoleMixin):
    # def filter_by_admin(self, q, params):
    #     return q.join(DocType, DocType.doc_type_id == Model.doc_type_id) \
    #         .filter(DocType.status, DocType.creator_id == g.user_id)

    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取模型记录，分页
        """
        user_role = self.get_current_role()
        if args.get("doc_type_id"):  # 获取某个doc_type项目的模型列表
            count, result = ModelService().get_train_job_list_by_doc_type_id(
                doc_type_id=args['doc_type_id'], search=args['query'], offset=args['offset'], limit=args['limit'])
        else:  # 获取全部的模型列表
            count, result = ModelService().get_train_job_list_by_nlp_task(
                nlp_task='wordseg', search=args['query'], offset=args['offset'], limit=args['limit'])
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "model_name": fields.String(required=True),
        "model_desc": fields.String(missing=""),
        "doc_type_id": fields.Integer(required=True),
        "model_train_config": fields.Raw(required=True),
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        创建模型
        """
        result = ModelService().create_train_job_by_doc_type_id(
            doc_type_id=args["doc_type_id"], train_job_name=args["model_name"], train_job_desc=args["model_desc"],
            train_config=args["model_train_config"], mark_job_ids=args["mark_job_ids"])
        return {
                   "message": "创建成功",
                   "result": result
               }, 201
