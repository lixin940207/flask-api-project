# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:39 下午
import json
from flask import g
from app.common.redis import r
from app.common.log import logger
from app.config.config import get_config_from_app as _get
from app.common.extension import session
from app.common.fileset import upload_fileset
from app.common.seeds import NlpTaskEnum, StatusEnum
from app.model.mark_task_model import MarkTaskModel
from app.model.doc_type_model import DocTypeModel
from app.model.custom_algorithm_model import CustomAlgorithmModel
from app.model.train_job_model import TrainJobModel
from app.model.train_task_model import TrainTaskModel
from app.model.train_term_task_model import TrainTermTaskModel
from app.schema.custom_algorithm_schema import CustomAlgorithmSchema
from app.schema.doc_type_schema import DocTypeSchema
from app.schema.train_job_schema import TrainJobSchema
from app.common.utils.time import get_now_with_format


class ModelService:
    @staticmethod
    def get_train_job_list_by_nlp_task(nlp_task, search, offset, limit):
        # get nlp_task id
        nlp_task_id = int(getattr(NlpTaskEnum, nlp_task))
        # get train jobs by nlp_task id and other filters
        train_jobs = TrainJobModel().get_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search, offset=offset,
                                                        limit=limit)
        # count train jobs by nlp_task_id and other filters
        count = TrainJobModel().count_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search)
        # assign doc_type to each train job for dumping
        for train_job in train_jobs:
            train_job.doc_type = DocTypeModel().get_by_id(train_job.doc_type_id)
        # get the serialized result
        result = TrainJobSchema().dump(train_jobs, many=True)
        return count, result

    @staticmethod
    def get_train_job_list_by_doc_type_id(doc_type_id, search, offset, limit):
        # verify doc type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # get train jobs by nlp_task id and other filters
        train_jobs = TrainJobModel().get_by_filter(search=search, offset=offset,
                                                   limit=limit, doc_type_id=doc_type_id)
        # count train jobs by nlp_task_id and other filters
        count = TrainJobModel().count_by_filter(search=search, doc_type_id=doc_type_id)
        # assign doc_type to each train job for dumping
        for train_job in train_jobs:
            train_job.doc_type = doc_type
        # get the serialized result
        result = TrainJobSchema().dump(train_jobs, many=True)
        return count, result

    @staticmethod
    def create_classify_train_job_by_doc_type_id(doc_type_id, train_job_name, train_job_desc, train_config, mark_job_ids,
                                     custom_id):
        # verify doc_type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # get nlp_task name
        nlp_task = "classify"
        # generate model version by nlp task
        model_version = generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task)

        # create TrainJob table
        train_job = TrainJobModel().create(
            train_job_name=train_job_name,
            train_job_desc=train_job_desc,
            doc_type_id=doc_type_id,
            train_job_status=int(StatusEnum.processing)
        )
        # create TrainTask table
        train_task = TrainTaskModel().create(
            train_job_id=train_job.train_job_id,
            train_model_name=train_job_name,
            train_model_desc=train_job_desc,
            train_config=train_config,
            train_status=int(StatusEnum.processing),
            mark_job_ids=mark_job_ids,
            model_version=model_version
        )

        if custom_id:
            custom_item = CustomAlgorithmModel().get_by_id(custom_id)
            custom = CustomAlgorithmSchema(
                only=("custom_algorithm_alias", "custom_algorithm_ip", "custom_algorithm_predict_port")).dump(
                custom_item)
        else:
            custom = None

        # push to redis
        push_train_task_to_redis(nlp_task, doc_type_id, train_task.train_task_id, model_version, train_config, mark_job_ids, custom)
        session.commit()

        # add some attribute for dumping
        train_job.train_list = [train_task]
        train_job.doc_type = doc_type
        train_job.model_version = model_version
        result = TrainJobSchema().dump(train_job)
        return result

    @staticmethod
    def create_train_job_by_doc_type_id(doc_type_id, train_job_name, train_job_desc, train_config, mark_job_ids):
        # verify doc_type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # get nlp_task name
        nlp_task = NlpTaskEnum(doc_type.nlp_task_id).name
        # generate model version by nlp task
        model_version = generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task)

        # 为model_train_config补充model_version字段，供后台服务处理
        for config in train_config:
            config['version'] = model_version

        # create TrainJob table
        train_job = TrainJobModel().create(
            train_job_name=train_job_name,
            train_job_desc=train_job_desc,
            doc_type_id=doc_type_id,
            train_job_status=int(StatusEnum.processing)
        )
        # create TrainTask table
        train_task = TrainTaskModel().create(
            train_job_id=train_job.train_job_id,
            train_model_name=train_job_name,
            train_model_desc=train_job_desc,
            train_config=train_config,
            train_status=int(StatusEnum.processing),
            mark_job_ids=mark_job_ids,
            model_version=model_version
        )
        if nlp_task in ["extract", "relation"]:
            # create TrainTermTask table for each doc term
            train_term_task_list = []
            for field_config in train_config:
                train_term_task_list.append({
                    "train_task_id": train_task.train_task_id,
                    "doc_term_id": field_config["field_id"],
                    "train_term_status": int(StatusEnum.processing)
                })
            TrainTermTaskModel().bulk_create(train_term_task_list)

        # push to redis
        push_train_task_to_redis(nlp_task, doc_type_id, train_task.train_task_id, model_version, train_config, mark_job_ids)
        session.commit()

        # add some attribute for dumping
        train_job.train_list = [train_task]
        train_job.doc_type = doc_type
        train_job.model_version = model_version
        result = TrainJobSchema().dump(train_job)
        return result


def generate_model_version_by_nlp_task(doc_type_id, mark_job_ids, nlp_task):
    mark_job_ids_str = ','.join([str(i) for i in mark_job_ids])
    if len(mark_job_ids_str) > 50:
        mark_job_ids_str = 'hash' + str(hash(mark_job_ids_str))
    if nlp_task == "extract":
        return "{}_NER{}_{}".format(get_now_with_format(), doc_type_id, mark_job_ids_str)
    elif nlp_task == "classify":
        return "{}_{}_{}".format(get_now_with_format(), g.app_id, doc_type_id)
    elif nlp_task == "relation":
        return "{}_RE{}_{}".format(get_now_with_format(), doc_type_id, mark_job_ids_str)
    elif nlp_task == "wordseg":
        return '{}_WS{}_{}'.format(get_now_with_format(), doc_type_id, mark_job_ids_str)


def push_train_task_to_redis(nlp_task, doc_type_id, train_task_id, model_version, train_config, mark_job_ids, custom=None):
    if nlp_task == "classify":
        r.lpush(_get('CLASSIFY_MODEL_QUEUE_KEY'), json.dumps({
            "version": model_version,
            "task_type": 'train',
            "event_id": train_task_id,
            "configs": train_config,
            "data_path": generate_classify_data(mark_job_ids),
            "label": DocTypeSchema().dump(DocTypeModel().get_by_id(doc_type_id)),
            "custom": custom,
            "use_rule": 0,
        }))
    else:
        prefix_map = {"extract": "NER", "relation": "RE", "wordseg": "WS"}
        r.lpush(_get("{}_TRAIN_QUEUE_KEY".format(nlp_task.upper())), json.dumps({
            "version": model_version,
            "doctype": prefix_map[nlp_task] + str(doc_type_id),
            "tasks": mark_job_ids,
            "model_type": nlp_task,
            "configs": [json.dumps(x) for x in train_config],
        }))


def generate_classify_data(mark_job_ids):
    # name = generate_unique_name('csv')
    # path = f"{upload_fileset.path}/{name}"
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
