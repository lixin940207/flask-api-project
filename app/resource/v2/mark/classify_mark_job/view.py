# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
import typing
from flask_restful import Resource
from app.common.patch import parse, fields
from app.service.classify_mark_job_service import ClassifyMarkJobService


class ClassifyMarkJobListResource(Resource):
    @parse({
        "is_superuser": fields.Boolean(missing=False),
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(missing=None),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        count, result = ClassifyMarkJobService().get_mark_job_list(args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200
