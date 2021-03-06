# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/1-11:20 上午
import requests
from flask_restful import abort

from app.common.extension import session
from app.config.config import get_config_from_app as _get
from app.common.common import StatusEnum
from app.entity import TrainTask, TrainTermTask
from app.model import TrainTaskModel, TrainJobModel
from app.model.train_m2m_mark_model import TrainM2mMarkbModel
from app.model.train_term_task_model import TrainTermTaskModel


class ModelTrainService():
    @staticmethod
    def get_train_task_list_by_train_job_id(train_job_id, order_by, order_by_desc, offset, limit) -> (int, [TrainTask]):
        count, result = TrainTaskModel().get_by_filter(order_by=order_by, order_by_desc=order_by_desc, offset=offset, limit=limit, train_job_id=train_job_id)
        return count, result

    @staticmethod
    def get_train_task_by_id(train_task_id) -> TrainTask:
        train_task = TrainTaskModel().get_by_id(train_task_id)
        train_task.mark_job_ids = [m2m.mark_job_id for m2m in TrainM2mMarkbModel().get_by_filter(limit=99999, train_job_id=train_task.train_job_id)]
        return train_task

    @staticmethod
    def get_train_term_list_by_train_task_id(train_task_id, **kwargs) -> (int, [TrainTermTask]):
        count, result = TrainTermTaskModel().get_by_filter(limit=99999, train_task_id=train_task_id, **kwargs)
        return count, result

    @staticmethod
    def add_algo_dict_for_extract_relation(train_task_result):
        unique_algo_dict = dict()
        relation_unique_algo_dict = dict()
        train_type = train_task_result["model_train_config"][0]["train_type"]
        result_body = {}
        for field in train_task_result["model_train_config"]:
            algo_name = field["selectAlgorithms"]
            algo_name.sort()
            algo_name = ",".join(algo_name)
            if field["train_type"] in ["relation"]:
                if algo_name in relation_unique_algo_dict:
                    relation_unique_algo_dict[algo_name].append(field["field_name"])
                else:
                    relation_unique_algo_dict[algo_name] = [field["field_name"]]
            else:
                if algo_name in unique_algo_dict:
                    unique_algo_dict[algo_name].append(field["field_name"])
                else:
                    unique_algo_dict[algo_name] = [field["field_name"]]
        result_body["model_fields"] = [{"train_type": train_type, "algorithm": key.split(","), "fields": val} for
                                       key, val in unique_algo_dict.items()]
        result_body["model_fields"].extend(
            [{"train_type": "relation", "algorithm": key.split(","), "fields": val} for key, val in
             relation_unique_algo_dict.items()])

        result = result_body
        return result

    @staticmethod
    def update_train_task_term_by_id(train_term_task_id, args):
        train_term_task = TrainTermTaskModel().update(train_term_task_id, **args)
        session.commit()
        return train_term_task

    @staticmethod
    def update_train_task_by_id(train_job_id, train_task_id, is_check_train_terms, model_type, args):
        """
        1. 根据字段状态更新训练状态和结果
        2. 直接设置训练状态和结果
        3. 模型上线状态更新（分类和抽取还不一样）
        """
        train_job = TrainJobModel().get_by_id(train_job_id)
        train_task = TrainTaskModel().get_by_id(train_task_id)

        if is_check_train_terms: # 是否需要检查train_term的状态
            _, training_terms = TrainTermTaskModel().get_by_filter(limit=99999, train_task_id=train_task_id,
                                                                   train_term_status=int(StatusEnum.training))
            _, failed_terms = TrainTermTaskModel().get_by_filter(limit=99999, train_task_id=train_task_id,
                                                                 train_term_status=int(StatusEnum.fail))
            if not training_terms:
                # 没有处于训练中
                if not failed_terms:
                    # 没有处于失败的
                    args["train_status"] = int(StatusEnum.success)
                else:
                    args["train_status"] = int(StatusEnum.fail)
            else:
                args["train_status"] = int(StatusEnum.training)
        else:
            # no limit to set model_train_state=success/failed
            if args["train_status"] == int(StatusEnum.online):
                # validation
                if train_task.train_status == StatusEnum.online:
                    abort(400, message="该模型已经上线")
                if train_task.train_status != StatusEnum.success:
                    abort(400, message="只能上线训练成功的模型")

                # send model train http request
                service_url = _get("CLASSIFY_MODEL_ONLINE") if model_type == "classify" else _get("EXTRACT_MODEL_ONLINE")
                resp = requests.post(f"{service_url}?model_version={train_task.model_version}")
                if resp.status_code < 200 or resp.status_code >= 300:
                    abort(500, message=f"上线服务 <{service_url}> 出现错误: {resp.text}")

                # find all online model under this doc_type_id
                online_models = TrainTaskModel().get_by_doc_type_id(doc_type_id=train_job.doc_type_id, train_status=int(StatusEnum.online))

                # unload online models
                TrainTaskModel().bulk_update([train.train_task_id for train in online_models], train_status=int(StatusEnum.success))

        # update train task
        train_task = TrainTaskModel().update(train_task_id, **args)
        session.commit()
        return train_task

    @staticmethod
    def update_train_term_by_model_version_and_doc_term_id(model_version, doc_term_id, args):
        train_term = TrainTermTaskModel().get_by_model_version_and_doc_term_id(model_version=model_version, doc_term_id=doc_term_id)
        train_term_task = TrainTermTaskModel().update(train_term.train_term_task_id, **args)
        session.commit()
        return train_term_task

    @staticmethod
    def update_train_task_by_model_version(model_version, is_check_train_terms, args):
        train_task = TrainTaskModel().get_by_filter(model_version=model_version)[1][0]

        if is_check_train_terms:
            _, training_terms = TrainTermTaskModel().get_by_filter(limit=99999, train_task_id=train_task.train_task_id,
                                                                   train_term_status=int(StatusEnum.training))
            _, failed_terms = TrainTermTaskModel().get_by_filter(limit=99999, train_task_id=train_task.train_task_id,
                                                                 train_term_status=int(StatusEnum.fail))
            if not training_terms:
                # 没有处于训练中
                if not failed_terms:
                    # 没有处于失败的
                    args["train_status"] = int(StatusEnum.success)
                else:
                    args["train_status"] = int(StatusEnum.fail)
            else:
                args["train_status"] = int(StatusEnum.training)
        train_task = TrainTaskModel().update(train_task.train_task_id, **args)
        session.commit()
        return train_task

    @staticmethod
    def delete_train_task_by_id(train_task_id):
        TrainTaskModel().delete(train_task_id)
        session.commit()