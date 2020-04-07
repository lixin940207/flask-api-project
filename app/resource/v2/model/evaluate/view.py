# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/2-6:50 下午
import typing
from flask_restful import Resource

from app.common.common import StatusEnum
from app.common.patch import parse, fields
from app.schema.evaluate_task_schema import EvaluateTaskSchema
from app.service.model_evaluate_service import ModelEvaluateService


class ModelEvaluateListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg')),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(
            self: Resource,
            args: typing.Dict,
            model_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        获取模型评估记录，分页
        """
        order_by = args["order_by"][1:]
        order_by_desc = True if args["order_by"][0] == "-" else False
        count, evaluate_task_list = ModelEvaluateService().get_evaluate_task_list_by_train_job_id(train_job_id=model_id, order_by=order_by, order_by_desc=order_by_desc, offset=args["offset"], limit=args["limit"])
        # convert int status to string
        for evaluate_task in evaluate_task_list:
            evaluate_task.evaluate_task_status = StatusEnum(evaluate_task.evaluate_task_status).name
        result = EvaluateTaskSchema(many=True).dump(evaluate_task_list)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "model_evaluate_name": fields.String(required=True),
        "model_evaluate_desc": fields.String(missing=""),
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
        "doc_term_ids": fields.List(fields.Integer(), missing=[]),
        "doc_relation_ids": fields.List(fields.Integer(), missing=[]),
        "use_rule": fields.Integer(missing=0),  # 分类专用: 默认不使用规则
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ['extract', 'classify', 'relation', 'wordseg']),
    })
    def post(
            self: Resource,
            args: typing.Dict,
            model_id: int,
    ) -> typing.Tuple[typing.Dict, int]:
        """
        创建一条评估记录
        """
        evaluate_task = ModelEvaluateService().create_evaluate_task_by_train_job_id(train_job_id=model_id, evaluate_task_name=args["model_evaluate_name"], evaluate_task_desc=args["model_evaluate_desc"],
                                                                    mark_job_ids=args["mark_job_ids"], doc_term_ids=args["doc_term_ids"], doc_relation_ids=args["doc_relation_ids"],
                                                                    use_rule=args["use_rule"])
        # convert int status to string
        evaluate_task.evaluate_task_status = StatusEnum(evaluate_task.evaluate_task_status).name
        result = EvaluateTaskSchema().dump(evaluate_task)
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ModelEvaluateItemResource(Resource):
    @parse({
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def get(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_evaluate_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        获取单条模型评估记录
        """
        evaluate_task = ModelEvaluateService().get_evaluate_task_by_id(model_evaluate_id)
        # convert int status to string
        evaluate_task.evaluate_task_status = StatusEnum(evaluate_task.evaluate_task_status).name
        result = EvaluateTaskSchema().dump(evaluate_task)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "model_evaluate_name": fields.String(),
        "model_evaluate_desc": fields.String(),
        "model_evaluate_state": fields.String(),
        "model_evaluate_result": fields.Dict(),
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def patch(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_evaluate_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        更新一条评估记录
        """
        update_params = {}
        if args.get("model_evaluate_state"):
            update_params.update(evaluate_task_status=int(StatusEnum[args["model_evaluate_state"]]))
        if args.get("model_evaluate_result"):
            update_params.update(evaluate_task_result=args["model_evaluate_result"])
        if args.get("model_evaluate_name"):
            update_params.update(evaluate_task_name=args["model_evaluate_name"])
        if args.get("model_evaluate_desc"):
            update_params.update(evaluate_task_desc=args["model_evaluate_desc"])
        evaluate_task = ModelEvaluateService().update_evaluate_task_by_id(evaluate_task_id=model_evaluate_id, args=update_params)
        # convert int status to string
        evaluate_task.evaluate_task_status = StatusEnum(evaluate_task.evaluate_task_status).name
        result = EvaluateTaskSchema().dump(evaluate_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    @parse({
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def delete(
            self: Resource,
            args: typing.Dict,
            model_id: int,
            model_evaluate_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        """
        删除一条评估记录
        """
        ModelEvaluateService().delete_evaluate_task_by_id(evaluate_task_id=model_evaluate_id)
        return {
                   "message": "删除成功",
               }, 200