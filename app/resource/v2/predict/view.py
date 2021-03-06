# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:21 下午
import typing
from flask_restful import Resource
from app.common.common import Common
from app.common.filters import CurrentUserMixin
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema import PredictJobSchema
from app.service.predict_service import PredictService


class ExtractJobListResource(Resource, CurrentUserMixin):
    @parse({
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "query": fields.String(missing=''),
        "doc_type_id": fields.Integer(missing=0),
        "order_by": fields.String(missing='-created_time'),
    })
    def get(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        nlp_task_id = Common().get_nlp_task_id_by_route()
        order_by = args["order_by"][1:]
        order_by_desc = True if args["order_by"][0] == "-" else False
        count, predict_job_list = PredictService().get_predict_job_list_by_nlp_task_id(nlp_task_id=nlp_task_id,
                                                                                       doc_type_id=args['doc_type_id'],
                                                                                       search=args['query'],
                                                                                       order_by=order_by, order_by_desc=order_by_desc,
                                                                                       offset=args['offset'], limit=args['limit'],
                                                                                       current_user=self.get_current_user())
        # get the serialized result
        result = PredictJobSchema().dump(predict_job_list, many=True)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "extract_job_name": fields.String(required=True),
        "extract_job_type": fields.String(required=True),
        "extract_job_desc": fields.String(missing=""),
        "doc_type_id": fields.Integer(required=True),
        "files": fields.List(fields.File(), required=True),
        "task_type": fields.String(required=True, validate=lambda x: x in ['machine', 'manual']),
        "use_rule": fields.Integer(missing=0)
    }, locations=('form', 'files'))
    def post(
            self: Resource,
            args: typing.Dict
    ) -> typing.Tuple[typing.Dict, int]:
        predict_job = PredictService().create_predict_job_by_doc_type_id(doc_type_id=args["doc_type_id"],
                                                                         predict_job_name=args["extract_job_name"],
                                                                         predict_job_desc=args["extract_job_desc"],
                                                                         predict_job_type=args["extract_job_type"],
                                                                         files=args["files"],
                                                                         use_rule=args["use_rule"])
        result = PredictJobSchema().dump(predict_job)
        return {
                   "message": "创建成功",
                   "result": result
               }, 201


class ExtractJobItemResource(Resource, CurrentUserMixin):
    def get(self: Resource, job_id: int) -> typing.Tuple[typing.Dict, int]:
        nlp_task_id = Common().get_nlp_task_id_by_route()

        # get predict job
        predict_job = PredictService().get_predict_job_by_id(nlp_task_id=nlp_task_id, predict_job_id=job_id, current_user=self.get_current_user)
        result = PredictJobSchema().dump(predict_job)
        return {
                   "message": "请求成功",
                   "result": result
               }, 200

    @parse({
        "extract_job_name": fields.String(),
        "extract_job_desc": fields.String(),
        "extract_job_state": fields.String(),
    })
    def patch(
            self: Resource,
            args: typing.Dict,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        update_params = {}
        if args.get("extract_job_name"):
            update_params.update(predict_job_name=args["extract_job_name"])
        if args.get("extract_job_desc"):
            update_params.update(predict_job_desc=args["extract_job_desc"])
        if args.get("extract_job_state"):
            update_params.update(predict_job_status=status_str2int_mapper()[args["extract_job_state"]])
        predict_job = PredictService().update_predict_job_by_id(predict_job_id=job_id, args=update_params)
        result = PredictJobSchema().dump(predict_job)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 200

    def delete(
            self: Resource,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:
        PredictService().delete_predict_job_by_id(predict_job_id=job_id)
        return {
                   "message": "删除成功",
               }, 200


class ExtractJobExportResource(Resource):
    @parse({
        "offset": fields.Integer(missing=50),
    })
    def get(
            self: Resource,
            args: typing.Dict,
            job_id: int
    ) -> typing.Tuple[typing.Dict, int]:

        nlp_task_id = Common().get_nlp_task_id_by_route()
        file_path = PredictService().export_predict_file(nlp_task_id=nlp_task_id, predict_job_id=job_id, offset=args["offset"])

        return {
                   "message": "请求成功",
                   "file_path": file_path
               }, 200
