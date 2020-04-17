# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-12:32 下午

import json
import typing

from flask_restful import Resource

from app.common.common import StatusEnum
from app.common.log import logger
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema import PredictTaskSchema, UserTaskSchema
from app.service.doc_service import DocService
from app.service.mark_job_service import MarkJobService
from app.service.predict_service import PredictService


class AsyncMQResource(Resource):
    @parse({
        "task_result": fields.Raw(),
        "message": fields.Raw(),
        "task_state": fields.String(required=True, validate=lambda x: x in ('success', 'failed')),
        "error_message": fields.String()
    })
    def post(self: Resource, args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        message queue回调统一入口
        """
        message = args['message']
        logger.info(f"receive callback info from mq. response is: {json.dumps(args)}")

        if message['business'] in [
            'label',  # 实体预标注
            'classify_label',  # 分类预标注
            'relation_label',  # 实体关系预标注
            'wordseg_label'  # 分词预标注
        ]:
            update_params = {}
            if args.get("task_state"):
                if args['task_state'] == 'success':     # 如果mq预标注返回成功，则初试状态是unlabel
                    update_params.update(mark_task_status=int(StatusEnum.unlabel))
                else:   # 如果mq预标注返回失败，则初试状态是fail
                    update_params.update(mark_task_status=int(StatusEnum.fail))
            if args.get("task_result"):
                update_params.update(mark_task_result=args["task_result"])
            mark_task, user_task_list = MarkJobService()\
                .update_mark_task_and_user_task_by_mark_task_id(mark_task_id=message["task_id"], args=update_params)
            MarkJobService().update_mark_job_status_by_mark_task(mark_task=mark_task)
            result = UserTaskSchema(many=True).dump(user_task_list)
            return {
                       "message": "更新成功",
                       "result": result,
                   }, 201
        elif message['business'] in [
            'extract',  # 实体抽取
            'classify_extract',  # 分类抽取
            'relation_extract',  # 实体关系抽取
            'wordseg_extract'  # 分词抽取
        ]:
            update_params = {}
            if args.get("task_state"):
                update_params.update(predict_task_status=status_str2int_mapper()[args["task_state"]])
            if args.get("task_result"):
                update_params.update(predict_task_result=args["task_result"])
            predict_task = PredictService().update_predict_task_by_id(predict_task_id=message["task_id"], args=update_params)
            result = PredictTaskSchema().dump(predict_task)
            return {
                       "message": "更新成功",
                       "result": result,
                   }, 201


class UpdateDocConvertStateResource(Resource):

    @parse({
        "convert_state": fields.String(missing='processing'),
        "doc_id": fields.Integer(required=True),
    })
    def post(self: Resource,
             args: typing.Dict) -> typing.Tuple[typing.Dict, int]:
        """
        更新文档的处理状态
        """
        DocService().update_doc_by_id(doc_id=args["doc_id"],
                                      **{"doc_status": status_str2int_mapper()[args["convert_state"]]})
        return {
            "message": "更新成功",
        }, 201