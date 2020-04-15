# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/13-10:40 上午
import typing

from flask_restful import Resource, abort

from app.common.common import StatusEnum, NlpTaskEnum, Common
from app.common.patch import parse, fields
from app.common.utils.name import get_ext
from app.entity.base import AssignModeEnum
from app.service.mark_job_service import MarkJobService


class WordsegMarkJobListResource(Resource):
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
        count, result = MarkJobService().get_mark_job_list_by_nlp_task(args, nlp_task=NlpTaskEnum.wordseg)
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
        "assessor_id": fields.Integer(missing=0),
        "labeler_ids": fields.List(fields.Integer(), required=True),
    }, locations=('form', 'files'))
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        files = args["files"]
        assign_mode = args["assign_mode"]
        if assign_mode == AssignModeEnum.together:
            abort(400, message="不支持共同标注")
        job_type = Common().check_job_type_by_files(files)
        if job_type != "text":
            abort(400, message="请上传纯文本文档（txt/csv）")
        else:
            args['mark_job_type'] = job_type
        try:
            result = MarkJobService().create_mark_job(files, NlpTaskEnum.wordseg, args)
            return {
                       "message": "创建成功",
                       "result": result
                   }, 201
        except TypeError:
            abort(400, message="上传文件类型错误")


class WordsegMarkJobItemResource(Resource):
    def delete(
            self: Resource,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        MarkJobService.delete_mark_job(job_id)
        return {
                   "message": "删除成功",
               }, 200


class WordsegMarkJobMultiDelete(Resource):
    @parse({
        "job_ids": fields.List(fields.Integer(), missing=[])
    })
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        MarkJobService.delete_mark_jobs(args['job_ids'])
        return {
                   "message": "删除成功",
               }, 200


class WordsegMarkJobImportResource(Resource):
    @parse({
        "mark_job_name": fields.String(required=True),
        "mark_job_type": fields.String(required=True),
        "mark_job_desc": fields.String(),
        "doc_type_id": fields.Integer(required=True),
        "files": fields.List(fields.File(), required=True),
        "task_type": fields.String(required=True, validate=lambda x: x in ['machine', 'manual']),
    }, locations=('form', 'files'))
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        """
        上传已标注数据
        """
        files = args['files']
        # validate file extensions
        for f in files:
            if get_ext(f.filename) not in ["txt"]:
                abort(400, message="上传已标注分词数据仅支持txt格式。")
        result = MarkJobService().import_mark_job(files, args)
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class WordsegMarkJobExportResource(Resource):
    def get(
            self: Resource,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:

        file_path = MarkJobService().export_mark_file(nlp_task_id=int(NlpTaskEnum.wordseg), mark_job_id=job_id)
        return {
                   "message": "请求成功",
                   "file_path": file_path
               }, 200


class WordsegMarkJobRePreLabelResource(Resource):
    @parse({
        "mark_job_ids": fields.String(required=True),
    })
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        mark_job_ids = args['mark_job_ids'].split(',')
        MarkJobService().re_pre_label_mark_job(mark_job_ids, nlp_task=NlpTaskEnum.wordseg)
        return {
                   "message": "请求成功",
               }, 200
