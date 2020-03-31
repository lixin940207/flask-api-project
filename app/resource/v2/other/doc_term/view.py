import typing
from flask_restful import Resource
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
