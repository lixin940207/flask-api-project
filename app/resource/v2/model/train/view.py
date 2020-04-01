# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:29 下午
import typing
from flask_restful import Resource
from app.common.patch import parse, fields
from app.schema.train_task_schema import TrainTaskSchema
from app.schema.train_term_task_schema import TrainTermTaskSchema
from app.service.model_train_service import ModelTrainService


class ModelTrainListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "model_type": fields.String(required=True, validate=lambda x: x in ("extract", "classify")),
        "order_by": fields.String(missing="-created_time"),
    })
    def get(
            self: Resource,
            args: typing.Dict,
            model_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        获取模型训练记录，分页
        """
        order_by = args["order_by"][1:]
        order_by_desc = True if args["order_by"][0] == "-" else False
        count, train_tasks = ModelTrainService().get_train_task_list_by_train_job_id(train_job_id=model_id, order_by=order_by, order_by_desc=order_by_desc, offset=args["offset"], limit=args["limit"])
        result = TrainTaskSchema(many=True).dump(train_tasks)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class ModelTrainItemResource(Resource):
    @parse({
        "model_type": fields.String(required=True, validate=lambda x: x in ("extract", "classify", "relation", "wordseg"))
    })
    def get(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_train_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        获取单条模型训练记录
        """
        result = ModelTrainService().get_train_task_item_by_id(train_task_id=model_train_id, args=args)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "model_train_state": fields.String(),
        "model_train_result": fields.Dict(),
        "check_train_terms": fields.Boolean(missing=False),
        "model_type": fields.String(required=True, validate=lambda x: x in ("extract", "classify", "relation", "wordseg"))
    })
    def patch(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_train_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        修改模型的状态和结果
        """
        train_task = ModelTrainService().update_train_task(train_job_id=model_id, train_task_id=model_train_id, args=args)
        result = TrainTaskSchema().dump(train_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201

    @parse({
        "model_type": fields.String(required=True, validate=lambda x: x in ("extract", "classify"))
    })
    def delete(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_train_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        删除模型
        """
        ModelTrainService().delete_train_task(train_task_id=model_train_id)
        return {
                   "message": "删除成功",
               }, 204


class TrainTermListResource(Resource):
    @parse({
        "model_type": fields.String(required=True, validate=lambda x: x in ('extract', 'classify'))
    })
    def get(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_train_id: int,
    ) -> typing.Tuple[typing.Dict, int]:
        """
        获取模型训练的所有字段
        """
        count, train_terms = ModelTrainService().get_train_term_list_by_train_task_id(train_task_id=model_train_id)
        result = TrainTermTaskSchema(many=True).dump(train_terms)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class TrainTermItemResource(Resource):
    @parse({
        "train_term_state": fields.String(),
        "train_term_result": fields.Dict(),
        "model_type": fields.String(required=True, validate=lambda x: x in ('extract', 'classify')),
    })
    def patch(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_train_id: int,
            train_term_id: int,
    ) -> typing.Tuple[typing.Dict, int]:
        """
        修改模型训练的一个字段状态
        """
        train_term_task = ModelTrainService().update_train_task_term(train_term_task_id=train_term_id, **args)
        result = TrainTermTaskSchema().dump(train_term_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201
