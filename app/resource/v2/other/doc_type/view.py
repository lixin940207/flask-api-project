import typing
from flask_restful import Resource
from app.common.patch import parse, fields
from app.common.filters import CurrentUserMixin
from app.common.common import Common
from app.service.doc_type_service import DocTypeService


class DocTypeListResource(Resource, CurrentUserMixin):

    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
        "is_online": fields.Integer()
    })
    def get(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有文档条款
        :param args:
        :return:
        """
        Common.get_nlp_task_id_by_route(args)
        result, count = DocTypeService().get_doc_type(self.get_current_user(), args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "doc_type_name": fields.String(required=True),
        "doc_type_desc": fields.String(),
        "group_id": fields.Integer(default=-1),
        "doc_term_list": fields.List(fields.Nested({
            "doc_term_name": fields.String(required=True),
            "doc_term_alias": fields.String(default=""),
            "doc_term_shortcut": fields.String(default="", validate=lambda x: len(x) < 2),
            "doc_term_color": fields.String(required=True),
            "doc_term_desc": fields.String(required=False, allow_none=True),
            "doc_term_data_type": fields.String(required=True),
        }), missing=[])
    })
    def post(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        创建一个文档类型包括它的条款
        """
        # args.update({
        #     'nlp_task_id': self.nlp_task_id
        # })
        Common.get_nlp_task_id_by_route(args)
        result = DocTypeService().create_doc_type(self.get_current_user(), args)
        return {
                   "message": "创建成功",
                   "result": result,
               }, 201

