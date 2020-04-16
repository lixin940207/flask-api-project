# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:39 下午
import json
from flask import g
from app.common.filters import CurrentUser
from app.common.redis import r
from app.common.log import logger
from app.config.config import get_config_from_app as _get
from app.common.extension import session
from app.common.fileset import upload_fileset
from app.common.common import NlpTaskEnum, StatusEnum
from app.model import DocTermModel, EvaluateTaskModel
from app.model.mark_task_model import MarkTaskModel
from app.model.doc_type_model import DocTypeModel
from app.model.custom_algorithm_model import CustomAlgorithmModel
from app.model.train_job_model import TrainJobModel
from app.model.train_m2m_mark_model import TrainM2mMarkbModel
from app.model.train_task_model import TrainTaskModel
from app.model.train_term_task_model import TrainTermTaskModel
from app.schema import CustomAlgorithmSchema, DocTypeSchema, DocTermSchema
from app.common.utils.time import get_now_with_format


class ModelService:
    @staticmethod
    def get_train_job_list_by_nlp_task_id(nlp_task_id, doc_type_id, search, offset, limit, current_user: CurrentUser):
        # if exists doc_type_id, get train jobs of this doc_type_id
        if doc_type_id:
            count, train_job_list = TrainJobModel().get_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search, offset=offset,
                                                                     limit=limit, current_user=current_user, doc_type_id=doc_type_id)
        else:  # else get all
            count, train_job_list = TrainJobModel().get_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search, offset=offset,
                                                                     limit=limit, current_user=current_user)
        return count, train_job_list

    @staticmethod
    def create_classify_train_job_by_doc_type_id(doc_type_id, train_job_name, train_job_desc, train_config,
                                                 mark_job_ids,
                                                 custom_id):
        # verify doc_type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # get nlp_task name
        nlp_task = NlpTaskEnum.classify
        # generate model version by nlp task
        model_version = generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task)

        # create TrainJob table
        train_job = TrainJobModel().create(
            train_job_name=train_job_name,
            train_job_desc=train_job_desc,
            doc_type_id=doc_type_id,
            train_job_status=int(StatusEnum.training),
            preprocess={}
        )
        # create TrainM2mMark table
        train_m2m_mark_list = [{"train_job_id": train_job.train_job_id, "mark_job_id": _id} for _id in mark_job_ids]
        TrainM2mMarkbModel().bulk_create(train_m2m_mark_list)

        # create TrainTask table
        train_task = TrainTaskModel().create(
            train_job_id=train_job.train_job_id,
            train_model_name=train_job_name,
            train_model_desc=train_job_desc,
            train_config=train_config,
            train_status=int(StatusEnum.training),
            model_version=model_version
        )
        # bulk create train term
        doc_term_list = DocTermModel().get_by_filter(limit=99999, doc_type_id=doc_type_id)
        TrainTermTaskModel().bulk_create([dict(train_task_id=train_task.train_task_id,
                                               doc_term_id=doc_term.doc_term_id,
                                               train_term_status=int(StatusEnum.training)) for doc_term in doc_term_list])
        # assign doc term list to doc type
        doc_type.doc_term_list = doc_term_list

        if custom_id:
            custom_item = CustomAlgorithmModel().get_by_id(custom_id)
            custom = CustomAlgorithmSchema(
                only=("custom_id_name", "custom_ip", "custom_port")).dump(
                custom_item)
        else:
            custom = {}

        # push to redis
        push_train_task_to_redis(nlp_task, doc_type, train_task.train_task_id, model_version, train_config,
                                 mark_job_ids, custom)
        session.commit()

        # add some attribute for dumping
        train_task.mark_job_ids = mark_job_ids
        train_job.train_list = [train_task]
        train_job.doc_type = doc_type
        train_job.model_version = model_version
        return train_job

    @staticmethod
    def create_train_job_by_doc_type_id(doc_type_id, train_job_name, train_job_desc, train_config, mark_job_ids):
        # verify doc_type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # get nlp_task name
        nlp_task = NlpTaskEnum(doc_type.nlp_task_id)
        # generate model version by nlp task
        model_version = generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task)

        preprocess_type = {"split_by_sentence": train_config[0].get("train_type", "") in ["ner", "wordseg"]}

        # 为model_train_config补充model_version字段，供后台服务处理
        for config in train_config:
            config['version'] = model_version

        # create TrainJob table
        train_job = TrainJobModel().create(
            train_job_name=train_job_name,
            train_job_desc=train_job_desc,
            doc_type_id=doc_type_id,
            train_job_status=int(StatusEnum.training),
            preprocess=preprocess_type
        )
        # bulk create TrainM2mMark table
        train_m2m_mark_list = [{"train_job_id": train_job.train_job_id, "mark_job_id": _id} for _id in mark_job_ids]
        TrainM2mMarkbModel().bulk_create(train_m2m_mark_list)
        # create TrainTask table
        train_task = TrainTaskModel().create(
            train_job_id=train_job.train_job_id,
            train_model_name=train_job_name,
            train_model_desc=train_job_desc,
            train_config=train_config,
            train_status=int(StatusEnum.training),
            model_version=model_version
        )
        if nlp_task in [NlpTaskEnum.extract, NlpTaskEnum.relation]:
            # create TrainTermTask table for each doc term
            train_term_task_list = []
            for field_config in train_config:
                train_term_task_list.append({
                    "train_task_id": train_task.train_task_id,
                    "doc_term_id": field_config["field_id"],
                    "train_term_status": int(StatusEnum.training)
                })
            TrainTermTaskModel().bulk_create(train_term_task_list)

        # push to redis
        push_train_task_to_redis(nlp_task, doc_type, train_task.train_task_id, model_version, train_config,
                                 mark_job_ids)
        session.commit()

        # add some attribute for dumping
        train_task.mark_job_ids = mark_job_ids
        train_job.train_list = [train_task]
        train_job.doc_type = doc_type
        train_job.model_version = model_version
        return train_job

    @staticmethod
    def get_train_job_by_id(_id):
        train_job = TrainJobModel().get_by_id(_id)
        train_job.doc_type = DocTypeModel().get_by_id(train_job.doc_type_id)
        _, train_task_list = TrainTaskModel().get_by_filter(train_job_id=train_job.train_job_id)
        train_job.model_version = train_task_list[0].model_version
        return train_job

    @staticmethod
    def delete_train_job_by_id(_id):
        TrainJobModel().delete(_id)
        session.commit()

    @staticmethod
    def get_online_model_info_by_doc_type_id(doc_type_id, current_user):
        return TrainTaskModel().get_online_model_info_by_doc_type_id(doc_type_id=doc_type_id, current_user=current_user)


def generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task):
    mark_job_ids_str = ','.join([str(i) for i in mark_job_ids])
    if len(mark_job_ids_str) > 50:
        mark_job_ids_str = 'hash' + str(hash(mark_job_ids_str))
    if nlp_task == NlpTaskEnum.extract:
        return "{}_NER{}_{}".format(get_now_with_format(), doc_type_id, mark_job_ids_str)
    elif nlp_task == NlpTaskEnum.classify:
        return "{}_{}_{}".format(get_now_with_format(), g.app_id, doc_type_id)
    elif nlp_task == NlpTaskEnum.relation:
        return "{}_RE{}_{}".format(get_now_with_format(), doc_type_id, mark_job_ids_str)
    elif nlp_task == NlpTaskEnum.wordseg:
        return '{}_WS{}_{}'.format(get_now_with_format(), doc_type_id, mark_job_ids_str)


def push_train_task_to_redis(nlp_task, doc_type, train_task_id, model_version, train_config, mark_job_ids,
                             custom=None):
    if nlp_task == NlpTaskEnum.classify:
        r.lpush(_get('CLASSIFY_MODEL_QUEUE_KEY'), json.dumps({
            "version": model_version,
            "task_type": 'train',
            "event_id": train_task_id,
            "configs": train_config,
            "data_path": generate_classify_data(mark_job_ids),
            "label": DocTypeSchema().dump(doc_type),
            "custom": custom,
            "use_rule": 0,
        }))
    else:
        prefix_map = {"extract": "NER", "relation": "RE", "wordseg": "WS"}
        r.lpush(_get("{}_TRAIN_QUEUE_KEY".format(nlp_task.name.upper())), json.dumps({
            "version": model_version,
            "doctype": prefix_map[nlp_task.name] + str(doc_type.doc_type_id),
            "tasks": mark_job_ids,
            "model_type": nlp_task.name,
            "configs": [json.dumps(x) for x in train_config],
        }))


def generate_classify_data(mark_job_ids):
    results = []
    for mark_task, doc in MarkTaskModel().get_mark_task_and_doc_by_mark_job_ids(mark_job_ids):
        uuid = doc.doc_unique_name.split('.')[0]
        if mark_task.mark_task_result and len(mark_task.mark_task_result) > 0:
            marked_label = next(filter(lambda x: x['marked'] == 1, mark_task.mark_task_result))
            label = marked_label['label_id']
        else:
            label = ""
        row = ["", label, uuid]
        results.append(row)
    file_path = upload_fileset.export_to_csv(results=results, header=["text", "label", "uuid"])
    logger.info(f'save classify csv file to {file_path}')
    return file_path
