# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
import typing
from flask_restful import Resource, abort

from app.common.common import Common, NlpTaskEnum
from app.common.patch import parse, fields
from app.common.utils.name import get_ext
from app.service.classify_mark_job_service import MarkJobService


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
        count, result = MarkJobService().get_mark_job_list_by_nlp_task(args, NlpTaskEnum.classify)
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

        result = MarkJobService().create_mark_job(files, NlpTaskEnum.classify, args)

        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ClassifyMarkJobItemResource(Resource):
    def delete(self: Resource, job_id: int) -> typing.Tuple[typing.Dict, int]:
        MarkJobService().delete_mark_job(job_id)

        return {
                   "message": "删除成功",
               }, 200


class ClassifyMarkJobMultiDelete(Resource):
    @parse({
        "job_ids": fields.List(fields.Integer(), missing=[])
    })
    def post(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        MarkJobService().delete_mark_jobs(args["job_ids"])

        return {
                   "message": "批量删除成功",
                   "result": args
               }, 200


class ClassifyMarkJobImportResource(Resource):
    @parse({
        "mark_job_name": fields.String(required=True),
        "mark_job_type": fields.String(required=True),
        "mark_job_desc": fields.String(),
        "doc_type_id": fields.Integer(required=True),
        "files": fields.List(fields.File(), required=True),
    }, locations=('form', 'files'))
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        files = args['files']
        for f in files:
            if get_ext(f.filename) not in ["csv"]:
                abort(400, message="已标注分类数据仅支持csv格式。")
        try:
            result = MarkJobService().import_mark_job(files, args)
            return {
                       "message": "创建成功",
                       "result": result
                   }, 201
        except UnicodeDecodeError:
            abort(400, message="文件编码错误 请上传utf-8编码文件")
        except KeyError:
            abort(400, message="文件格式不合规 请查看csv文件模版")


class ClassifyMarkJobExportResource(Resource):
    def get(
            self: Resource,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        file_path = MarkJobService().export_mark_file(nlp_task_id=int(NlpTaskEnum.classify), mark_job_id=job_id)
        return {
                   "message": "请求成功",
                   "file_path": file_path
               }, 200


class ClassifyMarkJobMultiExportResource(Resource):
    @parse({
        "job_ids": fields.List(fields.Integer(), missing=[])
    })
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        file_path = MarkJobService().export_multi_mark_file(nlp_task_id=int(NlpTaskEnum.classify), mark_job_id_list=args["job_ids"])
        return {
                   "message": "请求成功",
                   "file_path": file_path
               }, 200

    
class ClassifyMarkJobRePreLabelResource(Resource):
    @parse({
        "mark_job_ids": fields.String(required=True),
    })
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        mark_job_ids = args['mark_job_ids'].split(',')
        MarkJobService().re_pre_label_mark_job(mark_job_ids, nlp_task=NlpTaskEnum.classify)
        return {
                    "message": "请求成功",
                }, 200
