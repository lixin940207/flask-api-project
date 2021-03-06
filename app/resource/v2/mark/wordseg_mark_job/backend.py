import typing
from flask_restful import Resource

from app.common.patch import parse, fields
from app.service.mark_job_service import MarkJobService


class GetWordsegMarkJobDataResource(Resource):
    @parse({
        "mark_job_ids": fields.List(fields.Integer(), missing=[]),
    })
    def get(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        items = MarkJobService().get_mark_job_data_by_ids(args["mark_job_ids"], args, prefix="WS")
        return {
                   "message": "请求成功",
                   "result": items,
                   "count": len(items),
               }, 200
