import typing
from flask_restful import Resource, abort
from app.common.log import logger
from app.common.patch import parse, fields
from app.schema.doc_schema import DocSchema
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
        try:
            item = DocService().get_by_id(doc_id)
            result = DocSchema().dump(item)
        except Exception as e:
            logger.exception(e)
            abort()
        return {
                   "message": "请求成功",
                   "result": result,
               }, 200
