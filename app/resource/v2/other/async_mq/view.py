# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-12:32 下午

import json
import typing

from flask_restful import Resource

from app.common.log import logger
from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema.predict_task_schema import PredictTaskSchema
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
            # return SyncManualTaskResource().patch(
            #     task_id=message['task_id']
            # )
            pass
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