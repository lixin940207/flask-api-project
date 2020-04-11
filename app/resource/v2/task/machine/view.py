# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-12:40 下午
import typing
from flask_restful import Resource
from app.common.filters import CurrentUserMixin
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema.predict_task_schema import PredictTaskSchema
from app.service.task_machine_service import TaskMachineService

AVAILABLE_EXTRACT_JOB_TYPES = ['extract', 'classify_extract', 'relation_extract', 'wordseg_extract']


class MachineTaskListResource(Resource, CurrentUserMixin):
    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        'order_by': fields.String(missing='-created_time'),
        "job_type": fields.String(required=True, validate=lambda x: x in AVAILABLE_EXTRACT_JOB_TYPES),
        "task_state": fields.String(),
        "doc_type_id": fields.Integer(),
        "extract_job_id": fields.Integer(required=True),
    })
    def get(self: Resource, args: typing.Dict):
        order_by = args["order_by"][1:]
        order_by_desc = True if args["order_by"][0] == "-" else False
        filtered_list = {}
        if args.get("task_state"):
            filtered_list.update(predict_task_status=status_str2int_mapper()[args["task_state"]])
        count, predict_task_list = TaskMachineService().get_predict_task_list_by_predict_job_id(predict_job_id=args["extract_job_id"],
                                                                  search=args['query'],
                                                                  order_by=order_by, order_by_desc=order_by_desc,
                                                                  offset=args['offset'], limit=args['limit'],
                                                                  current_user=self.get_current_user(),
                                                                  args=filtered_list)
        result = PredictTaskSchema(many=True, exclude=('task_result',)).dump(predict_task_list)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class MachineTaskItemResource(Resource):
    def get(
            self: Resource,
            task_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        predict_task = TaskMachineService().get_predict_task_by_id(predict_task_id=task_id)
        result = PredictTaskSchema().dump(predict_task)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "task_state": fields.String(),
        "task_result": fields.Raw(),
    })
    def patch(
            self: Resource,
            args: typing.Dict,
            task_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        update_params = {}
        if args.get("task_state"):
            update_params.update(predict_task_status=status_str2int_mapper()[args["task_state"]])
        if args.get("task_result"):
            update_params.update(predict_task_result=args["task_result"])
        predict_task = TaskMachineService().update_predict_task_by_id(predict_task_id=task_id, args=update_params)
        result = PredictTaskSchema().dump(predict_task)
        # 根据task更新整个predict_job的状态
        TaskMachineService().update_predict_job_status_by_predict_task(predict_task=predict_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    def delete(
            self: Resource,
            task_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        predict_task = TaskMachineService().delete_predict_task_by_id(predict_task_id=task_id)
        # 根据task更新整个predict_job的状态
        TaskMachineService().update_predict_job_status_by_predict_task(predict_task=predict_task)
        return {
                   "message": "删除成功",
               }, 200
