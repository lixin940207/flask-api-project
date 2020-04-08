import typing
from flask_restful import Resource
from app.common.patch import parse, fields
from app.common.extension import session
from app.resource.v1.common.validator import check_doc_term_include
from app.schema.DocSchema import DocSchema
from sqlalchemy import and_
from app.service.doc_service import DocService


class DocListResource(Resource):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_ids": fields.List(fields.Integer(), missing=[]),  # ...?doc_ids=1&doc_ids=2
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
        "doc_term_ids": fields.List(fields.Integer(), missing=[]),
    })
    def get(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        获取所有文档，可以按照[doc_id]进行过滤
        """
        items, count = DocService().get_docs(args)

        result = DocSchema(many=True).dump(items)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200


class DocItemResource(Resource):
    def get(self: Resource, doc_id: int) -> typing.Tuple[typing.Dict, int]:
        """
        获取单个文档
        """
        item = DocService().get_by_id(doc_id)
        result = DocSchema().dump(item)
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200
