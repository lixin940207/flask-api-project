import typing
from flask_restful import Resource
from app.common.patch import parse, fields
from app.common.filters import CurrentUserMixin
from app.common.common import Common
from app.service.doc_type_service import DocTypeService
from app.schema.doc_type_schema import DocTypeSchema


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
        nlp_task_id = Common().get_nlp_task_id_by_route(args)
        args.update({
            'nlp_task_id': nlp_task_id
        })
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
        nlp_task_id = Common().get_nlp_task_id_by_route(args)
        args.update({
            'nlp_task_id': nlp_task_id
        })
        result = DocTypeService().create_doc_type(self.get_current_user(), args)
        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class DocTypeItemResource(Resource, CurrentUserMixin):
    def get(self: Resource, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        获取一个文档类型
        """
        nlp_task_id = Common().get_nlp_task_id_by_route()
        result = DocTypeService().get_doc_type_items(doc_type_id, nlp_task_id)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200

    @parse({
        "doc_type_name": fields.String(),
        "doc_type_desc": fields.String(),
        "doc_term_list": fields.List(fields.Nested({
            "doc_term_name": fields.String(required=True),
            "doc_term_alias": fields.String(default=""),
            "doc_term_color": fields.String(required=True),
            "doc_term_index": fields.Integer(required=True),
            "doc_term_id": fields.Integer(required=False),
            "doc_term_desc": fields.String(required=False, allow_none=True),
            "doc_term_data_type": fields.String(required=True),
        }))
    })
    def patch(self: Resource, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        修改一个文档类型，不包括修改它的条款
        """
        result = DocTypeService().update_doc_type(args, doc_type_id)

        return {
                   "message": "更新成功",
                   "result": result,
               }, 201

    def delete(self: Resource, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        删除一个文档类型
        """
        DocTypeService().delete_doc_type(doc_type_id)
        return {
                   "message": "删除成功",
               }, 204


class TopDocTypeResource(Resource):
    def patch(self: Resource, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        置顶一个文档类型，简单修改index=max+1
        """
        result = DocTypeService().set_favoriate_doc_type(doc_type_id, True)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201


class CancelTopDocTypeResource(Resource):
    def patch(self: Resource, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        取消置顶一个文档类型，简单修改index=0
        """
        result = DocTypeService().set_favoriate_doc_type(doc_type_id, False)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201


class CheckDocTypeItemResource(Resource):
    @parse({
        "doc_type_name": fields.String(required=True),
    })
    def post(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        检查文档类型是否合法和重复，暂时只检查名称是否重复
        """
        item = DocTypeService().check_doc_type_name_exists(args['doc_type_name'])
        return {
                   "message": "请求成功",
                   "result": {
                       "existed": bool(item)
                   },
               }, 200