from flask_restful import Resource

from app.common.patch import parse, fields
from app.common.utils.status_mapper import status_str2int_mapper
from app.schema.train_task_schema import TrainTaskSchema
from app.schema.train_term_task_schema import TrainTermTaskSchema
from app.service.model_train_service import ModelTrainService


class UpdateTrainTermResource(Resource):
    @parse({
        "model_version": fields.String(required=True),
        "doc_term_id": fields.Integer(required=True),
        "train_term_state": fields.String(required=True),
        "train_term_result": fields.Dict(),
        "term_type": fields.String(required=True),
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def put(self, args):
        """
        修改模型训练的一个字段状态
        """
        update_params = {}
        if args.get("train_term_state"):
            update_params.update(train_term_status=status_str2int_mapper()[args["train_term_state"]])
        if args.get("train_term_result"):
            update_params.update(train_term_result=args["train_term_result"])
        train_term_task = ModelTrainService().update_train_term_by_model_version_and_doc_term_id(model_version=args["model_version"],
                                                                                                 doc_term_id=args["doc_term_id"],
                                                                                                 args=update_params)
        result = TrainTermTaskSchema().dump(train_term_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201


class UpdateModelTrainResource(Resource):
    @parse({
        "model_version": fields.String(required=True),
        "check_train_terms": fields.Boolean(required=True),
        "model_train_state": fields.String(),
        "model_train_result": fields.Dict(),
        "model_type": fields.String(required=True,
                                    validate=lambda x: x in ('extract', 'classify', 'relation', 'wordseg'))
    })
    def put(self, args):
        """
        修改模型的状态
        """
        update_params = {}
        if args.get("model_train_state"):
            # 后端返回结果转换，失败时后端目前还返回failed
            update_params.update(train_status=status_str2int_mapper()[args["model_train_state"]])
        train_task = ModelTrainService().update_train_task_by_model_version(model_version=args["model_version"], is_check_train_terms=args["check_train_terms"], args=update_params)
        result = TrainTaskSchema().dump(train_task)
        return {
                   "message": "更新成功",
                   "result": result,
               }, 201
