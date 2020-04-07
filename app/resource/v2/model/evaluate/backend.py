# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/2-6:50 下午
from flask_restful import Resource
from app.common.patch import parse, fields
from app.schema.evaluate_task_schema import EvaluateTaskSchema
from app.service.model_evaluate_service import ModelEvaluateService


class UpdateModelEvaluateResource(Resource):
    @parse({
        "model_evaluate_id": fields.Integer(required=True),
        "model_evaluate_state": fields.String(required=True),
        "model_evaluate_result": fields.Dict(),
        "model_type": fields.String(required=True, validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def put(self, args):
        """
        更新一条评估记录
        """
        update_params = {}
        if args.get("model_evaluate_state"):
            update_params.update(evaluate_task_status=args["model_evaluate_state"])
        if args.get("model_evaluate_result"):
            update_params.update(evaluate_task_result=args["model_evaluate_result"])

        evaluate_task = ModelEvaluateService().update_evaluate_task_by_id(evaluate_task_id=args["model_evaluate_id"], args=update_params)
        result = EvaluateTaskSchema().dump(evaluate_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201