# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
import typing
from flask_restful import Resource, abort

from app.common.common import Common
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

    @parse({
        "mark_job_name": fields.String(required=True),
        "mark_job_type": fields.String(required=True),
        "mark_job_desc": fields.String(),
        "doc_type_id": fields.Integer(required=True),
        "files": fields.List(fields.File(), required=True),
        "assign_mode": fields.String(required=True, validate=lambda x: x in ['average', 'together']),
        "assessor_id": fields.Integer(),
        "labeler_ids": fields.List(fields.Integer(), required=True),
        "use_rule": fields.Integer(missing=1)  # 默认使用规则
    }, locations=('form', 'files'))
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        files = args['files']
        job_type = Common().check_job_type_by_files(files)
        if not job_type:
            abort(400, message='请上传全部纯文本文档（txt/csv）或者全部电子文档（pdf/word文档）')
        else:
            args['mark_job_type'] = job_type

        result = ClassifyMarkJobService().create_mark_job(files, args)

        return {
                   "message": "创建成功",
                   "result": result
               }, 201
