# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/13-10:40 上午
import typing

from flask_restful import Resource

from app.common.common import StatusEnum, NlpTaskEnum
from app.service.classify_mark_job_service import MarkJobService


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