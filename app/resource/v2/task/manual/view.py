# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: view.py 
@Time: 2020/04/11 13:54
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
import typing

from flask_restful import Resource

from app.common.filters import CurrentUserMixin
from app.common.patch import parse, fields
from app.service.manual_task_service import ManualTaskService


class ManualTaskItemResource(Resource):
    def delete(self, task_id):
        ManualTaskService().detele_task(task_id)
        return {
                   "message": "删除成功",
               }, 204


class RejectManualTaskResource(Resource):
    def put(self, task_id):
        ManualTaskService().reject_manual_task(task_id)
        return {
                   "message": "更新成功",
               }, 201


class TaskListResource(Resource, CurrentUserMixin):
    @parse({
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        'order_by': fields.String(missing='-task_id'),
        "doc_type_id": fields.Integer(),
        "job_id": fields.Integer(),
        "job_type": fields.String(required=True,
                                  validate=lambda x: x in (
                                          'mark', 'classify_mark', 'relation_mark', 'wordseg_mark')),
        "task_state": fields.String(missing="",
                                    validate=lambda x: x in ("", "processing", "failed", "success", "unaudit",
                                                             "audited", "unlabel"))
    })
    def get(self: Resource, args: typing.Dict):
        count, processed, result = ManualTaskService().get_user_task_or_mark_task_result_by_role(self.get_current_user(), args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
                   "processed": processed
               }, 200


class AssessTaskItemPdfPrintResource(Resource):
    def post(self, task_id: int):
        """
        导出审核员查看详情时，导出pdf
        :param task_id:
        :return:
        """
        pass
