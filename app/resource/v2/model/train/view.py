# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:29 下午
import typing
from flask_restful import Resource

from app.common.common import StatusEnum
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
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
        count, train_task_list = ModelTrainService().get_train_task_list_by_train_job_id(train_job_id=model_id, order_by=order_by, order_by_desc=order_by_desc, offset=args["offset"], limit=args["limit"])
        # convert int status to string
        for train_task in train_task_list:
            train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainTaskSchema(many=True).dump(train_task_list)
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
        # get single task task by id
        train_task = ModelTrainService().get_train_task_by_id(train_task_id=model_train_id)
        # convert int status to string
        train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainTaskSchema().dump(train_task)

        # add extra algorithm information for extract and relation.
        if args["model_type"] in ["extract", "relation"]:
            result = ModelTrainService().add_algo_dict_for_extract_relation(result)
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
        update_params = {}
        if args.get("model_train_state"): # 这里不考虑model_train_result因为新的表结构里没有这个列了
            update_params.update(train_status=status_str2int_mapper()[args["model_train_state"]])
        train_task = ModelTrainService().update_train_task_by_id(train_job_id=model_id, train_task_id=model_train_id,
                                                                 is_check_train_terms=args["check_train_terms"], model_type = args["model_type"],
                                                                 args=update_params)
        # convert int status to string
        train_task.train_status = StatusEnum(train_task.train_status).name
        result = TrainTaskSchema().dump(train_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

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
        ModelTrainService().delete_train_task_by_id(train_task_id=model_train_id)
        return {
                   "message": "删除成功",
               }, 200


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
        count, train_term_list = ModelTrainService().get_train_term_list_by_train_task_id(train_task_id=model_train_id)
        # convert int status to string
        for train_term in train_term_list:
            train_term.train_term_status = StatusEnum(train_term.train_term_status).name
        result = TrainTermTaskSchema(many=True).dump(train_term_list)
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
        update_params = {}
        if args.get("train_term_state"):
            update_params.update(train_term_status=status_str2int_mapper()[args["train_term_state"]])
        if args.get("train_term_result"):
            update_params.update(train_term_result=args["train_term_result"])
        train_term_task = ModelTrainService().update_train_task_term_by_id(train_term_task_id=train_term_id, args=update_params)
        # convert int status to string
        train_term_task.train_term_status = StatusEnum(train_term_task.train_term_status).name
        result = TrainTermTaskSchema().dump(train_term_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200
