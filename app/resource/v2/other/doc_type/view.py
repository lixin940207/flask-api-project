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
        nlp_task_id = Common().get_nlp_task_id_by_route()
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
        nlp_task_id = Common().get_nlp_task_id_by_route()
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
        result = DocTypeService().get_doc_type_items(doc_type_id)
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
    def patch(self: Resource, args: typing.Dict, doc_type_id: int) -> typing.Tuple[
        typing.Dict, int]:
        """
        修改一个文档类型，不包括修改它的条款
        """
        item = session.query(DocType).filter(DocType.doc_type_id == doc_type_id, DocType.status).one()
        item.update(**args)
        item.commit()

        doc_terms = session.query(DocTerm).filter(
            DocTerm.doc_type_id == item.doc_type_id
        ).all()

        new_items = []
        existed_items = []
        existed_ids = []

        for doc_term in args['doc_term_list']:
            if not doc_term.get('doc_term_id'):
                new_items.append(doc_term)
            else:
                existed_items.append(doc_term)
                existed_ids.append(doc_term['doc_term_id'])

        for doc_term in doc_terms:
            if doc_term.doc_term_id in existed_ids:
                index = existed_ids.index(doc_term.doc_term_id)
                doc_term.doc_term_index = existed_items[index]['doc_term_index']
                doc_term.doc_term_color = existed_items[index]['doc_term_color']
                doc_term.doc_term_name = existed_items[index]['doc_term_name']
                doc_term.doc_term_alias = existed_items[index]['doc_term_alias']
                doc_term.doc_term_data_type = existed_items[index]['doc_term_data_type']
                doc_term.status = True
            else:
                doc_term.status = False

        for new_item in new_items:
            DocTerm.create(**new_item, doc_type_id=item.doc_type_id)

        session.commit()

        result = DocTypeSchema().dump(item)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201

    def delete(self: Resource, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        删除一个文档类型
        """
        DocTypeService().delete_doc_term
        item = session.query(DocType).filter(DocType.doc_type_id == doc_type_id, DocType.status).one()
        item.delete()
        item.commit()
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
