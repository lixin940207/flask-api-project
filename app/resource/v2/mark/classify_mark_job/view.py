# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/23
import typing
from flask import g
from sqlalchemy import func
from flask_restful import Resource, abort
from app.common.filters import QueryByRoleMixin
from app.common.patch import parse, fields
from app.service.classify_mark_job_service import ClassifyMarkJobService


class ClassifyMarkJobListResource(Resource, QueryByRoleMixin):
    # def filter_by_admin(self, q, params):
    #     return q.filter(ClassifyMarkJob.creator_id == g.user_id)
    #
    # def filter_by_assess(self, q, params):
    #     return q.filter(ClassifyMarkJob.assessor_id == g.user_id)
    #
    # def filter_by_label(self, q, params):
    #     return q.filter(func.json_contains(ClassifyMarkJob.labeler_ids, str(g.user_id)))
    @parse({
        "is_superuser": fields.Boolean(missing=False),
        "query": fields.String(missing=''),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "doc_type_id": fields.Integer(),
        'order_by': fields.String(missing='-created_time'),
    })
    def get(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        count, result = ClassifyMarkJobService().get_mark_job_list(self.get_current_user_id(), self.get_current_role(),
                                                                   args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200
