import typing
from flask_restful import Resource

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
        result, count = DocTermService().get_doc_term_list(self.get_current_user_id(), self.get_current_role(), args)
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
        nlp_task_id = Common().get_nlp_task_id_by_route()
        if args.get('doc_term_ids'):
            result, count = DocTermService().get_doc_term_by_doctype(nlp_task_id, doc_type_id, args['offset'], args['limit'])
        else:
            result, count = DocTermService().get_doc_term_by_doctype(nlp_task_id, doc_type_id, args['offset'], args['limit'], doc_term_ids=args.get('doc_term_ids'))
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "doc_term_name": fields.String(required=True),
        "doc_term_color": fields.String(required=True),
        "doc_term_index": fields.Integer(required=True),
        "doc_term_data_type": fields.String(required=True),
    })
    def post(self, args: typing.Dict, doc_type_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        创建一个条款
        """
        nlp_task_id = Common().get_nlp_task_id_by_route()
        result = DocTermService().create_doc_term(nlp_task_id, args, doc_type_id)
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