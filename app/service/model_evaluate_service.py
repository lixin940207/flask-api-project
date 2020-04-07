# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/7-10:23 上午
import json
from app.common.redis import r
from app.common.extension import session
from app.config.config import get_config_from_app as _get
from app.common.common import NlpTaskEnum
from app.entity import EvaluateTask, TrainTask, DocType
from app.model import TrainTaskModel, TrainJobModel, DocTypeModel
from app.model.evaluate_task_model import EvaluateTaskModel
from app.schema.doc_type_schema import DocTypeSchema
from app.service.model_service import generate_classify_data


class ModelEvaluateService():
    @staticmethod
    def get_evaluate_task_by_id(_id):
        evaluate_task = EvaluateTaskModel().get_by_id(id)
        return evaluate_task

    @staticmethod
    def get_evaluate_task_list_by_train_job_id(train_job_id, order_by, order_by_desc, offset, limit):
        count, result = EvaluateTaskModel().get_by_train_job_id(train_job_id=train_job_id, order_by=order_by, order_by_desc=order_by_desc, offset=offset, limit=limit)
        return count, result

    @staticmethod
    def create_evaluate_task_by_train_job_id(train_job_id, evaluate_task_name, evaluate_task_desc, mark_job_ids, doc_term_ids, doc_relation_ids, use_rule=0):
        """
        如果后面要加重新训练的逻辑，这部分要改，不能根据train_job_id去创建评估任务，而是根据train_task_id，
        目前先保留，因为目前train_job和train_task是一一对应，不会有影响
        """
        # get correspondent train_job, doc_type, train_task, nlp_task by train_job_id
        train_job = TrainJobModel().get_by_id(train_job_id)
        doc_type = DocTypeModel().get_by_id(train_job.doc_type_id)
        nlp_task = NlpTaskEnum(doc_type.nlp_task_id)
        _, train_task_list = TrainTaskModel().get_by_filter(train_job_id=train_job_id)
        train_task = train_task_list[0]

        # create evaluate_task
        evaluate_task = EvaluateTaskModel().create(evaluate_task_name=evaluate_task_name, evaluate_task_desc=evaluate_task_desc, train_task_id=train_task.train_task_id)

        # push to evaluate redis queue
        push_evaluate_task_to_redis(nlp_task, evaluate_task, train_task, doc_type, mark_job_ids, doc_term_ids, doc_relation_ids, use_rule)
        session.commit()
        return evaluate_task

    @staticmethod
    def update_evaluate_task_by_id(evaluate_task_id, args):
        evaluate_task = EvaluateTaskModel().update(evaluate_task_id, **args)
        return evaluate_task

    @staticmethod
    def delete_evaluate_task_by_id(evaluate_task_id):
        EvaluateTaskModel().delete(evaluate_task_id)


def push_evaluate_task_to_redis(nlp_task, evaluate_task: EvaluateTask, train_task: TrainTask, doc_type: DocType, mark_job_ids, doc_term_ids, doc_relation_ids, use_rule):
    if nlp_task == NlpTaskEnum.classify:
        r.lpush(_get('CLASSIFY_MODEL_QUEUE_KEY'), json.dumps({
            "version": train_task.model_version,
            "task_type": 'evaluate',
            "event_id": evaluate_task.evaluate_task_id,
            "configs": train_task.train_config,
            "data_path": generate_classify_data(mark_job_ids),
            "label": DocTypeSchema().dump(doc_type),
            "use_rule": use_rule,
        }))
    else:
        push_dict = {
            "evaluate_id": evaluate_task.evaluate_task_id,
            "model_version": train_task.model_version,
            "tasks": mark_job_ids,
            "fields": doc_term_ids,
            'model_type': nlp_task.name,
            'model_reload_result': {},
        }
        if nlp_task == NlpTaskEnum.relation:
            push_dict.update({"relation_fields": doc_relation_ids})
        r.lpush(_get("{}_EVALUATE_QUEUE_KEY".format(nlp_task.name.upper())), json.dumps(push_dict))