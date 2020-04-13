import typing
from flask_restful import Resource, abort

from app.common.extension import session
from app.common.common import Common
from app.common.patch import parse, fields
from app.common.filters import CurrentUserMixin
from app.service.doc_term_service import DocTermService


class GetDocTermListResource(Resource, CurrentUserMixin):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "exclude_terms_ids": fields.List(fields.Integer(), missing=[]),
    })
    def get(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，分页，可选排除条件exclude_terms_ids
        """
        nlp_task_id = Common().get_nlp_task_id_by_route()
        args.update({
            'nlp_task_id': nlp_task_id
        })
        result, count = DocTermService().get_doc_term_list(args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class DocTermListResource(Resource, CurrentUserMixin):
    @parse({
        "doc_term_ids": fields.List(fields.Integer(), missing=[]),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
    })
    def get(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，不分页
        """
        if args.get('doc_term_ids'):
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'])
        else:
            result, count = DocTermService().get_doc_term_by_doctype(doc_type_id, args['offset'], args['limit'], doc_term_ids=args.get('doc_term_ids'))
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "doc_term_name": fields.String(required=True),
        "doc_term_color": fields.String(required=True),
        "doc_term_index": fields.Integer(required=True),
        "doc_term_desc": fields.String(default=""),
        "doc_term_data_type": fields.String(required=True),
    })
    def post(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        创建一个条款
        """
        result = DocTermService().create_doc_term(args, doc_type_id)
        return {
                   "message": "创建成功",
                   "result": result,
               }, 201


class ListWordsegDocTermResource(Resource, CurrentUserMixin):
    def get(self: Resource) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有条款，分页，可选排除条件exclude_terms_ids
        """
        result = Common().get_wordseg_doc_terms()
        return {
                   "message": "请求成功",
                   "result": result
               }, 200


class EntityDocTermItemResource(Resource):
    @parse({
        "doc_term_name": fields.String(),
        "doc_term_color": fields.String(),
        "doc_term_index": fields.Integer(),
        "doc_term_desc": fields.String(allow_none=True),
        "doc_term_data_type": fields.String(),
    })
    def patch(self: Resource, args: typing.Dict, doc_type_id: int, doc_term_id: int) -> typing.Tuple[
        typing.Dict, int]:
        """
        修改一个条款
        """
        result = DocTermService().update_doc_term(doc_type_id, doc_term_id, )
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201

    def delete(self: Resource, doc_type_id: int, doc_term_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        删除一个条款
        """
        if DocTermService().check_term_in_relation(doc_term_id):
            abort(400, message="该条款仍有关联关系，请确保条款没有关联关系后再做清除")

        DocTermService().remove_doc_term(doc_term_id)
        session.commit()
        return {
                   "message": "删除成功",
               }, 204
