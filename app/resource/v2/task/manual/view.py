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

from app.common.export import PDFAnnotationExport
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
        ManualTaskService().reject_mark_task(task_id)
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
        count, processed, result = ManualTaskService().get_user_task_or_mark_task_result_by_role(
            self.get_current_user(), args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
                   "processed": processed
               }, 200


class LabelTaskItemResource(Resource, CurrentUserMixin):
    def get(
            self: Resource,
            task_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        result = ManualTaskService().get_mark_task_or_user_task(self.get_current_user(), task_id)
        return {
                   "message": "请求成功",
                   "result": result
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
        """
        仅仅作为标注员保存自己的标注数据
        """
        result = ManualTaskService().update_user_task_status(self.get_current_user(), task_id, args)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201


class AssessTaskItemResource(Resource, CurrentUserMixin):
    def get(
            self: Resource,
            task_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        result = ManualTaskService().get_mark_task_or_user_task(self.get_current_user(), task_id)
        return {
                   "message": "请求成功",
                   "result": result
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
        """
        仅仅作为标注员保存自己的标注数据
        """
        result = ManualTaskService().update_mark_task_status(self.get_current_user(), task_id, args)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201


class TaskItemNextResource(Resource, CurrentUserMixin):

    @parse({
        "job_id": fields.Integer(),
        "job_type": fields.String(required=True,
                                  validate=lambda x: x in ('mark', 'classify_mark', 'relation_mark', 'wordseg_mark')),
        "task_state": fields.String(missing="",
                                    validate=lambda x: x in (
                                            "", "processing", "failed", "success", "unaudit", "audited",
                                            "unlabel")),
        "query": fields.String(missing=""),
    })
    def get(self: Resource, args: typing.Dict, task_id: int) -> typing.Tuple[typing.Dict, int]:
        preview_task_id, next_task_id = ManualTaskService().get_preview_and_next_task_id(self.get_current_user(),
                                                                                         task_id, args)

        return {
                   "message": "请求成功",
                   "next_id": next_task_id,
                   "prev_id": preview_task_id
               }, 200


class AssessTaskItemPdfPrintResource(Resource):
    def post(self, task_id: int):
        """
        导出审核员查看详情时，导出pdf
        :param task_id:
        :return:
        """
        doc_unique_name, doc_raw_name, labels = ManualTaskService().export_pdf(task_id)
        return PDFAnnotationExport(
            folder='upload',
            unique_name=doc_unique_name,
            file_name=doc_raw_name
        ).export_with_annotation(labels)
