# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:27 下午
import json
from flask_restful import abort

from app.common.extension import session
from app.config.config import get_config_from_app as _get
from app.common.common import StatusEnum
from app.common.fileset import upload_fileset
from app.common.filters import CurrentUser
from app.common.redis import r
from app.common.utils.name import get_ext
from app.entity import PredictJob
from app.entity.base import FileTypeEnum
from app.model import DocTypeModel, DocModel
from app.model.predict_job_model import PredictJobModel
from app.model.predict_task_model import PredictTaskModel


class PredictService:
    @staticmethod
    def get_predict_job_by_id(predict_job_id) -> PredictJob:
        predict_job = PredictJobModel().get_by_id(predict_job_id)
        # get all tasks under this predict job
        _, predict_task_list = PredictTaskModel().get_by_filter(limit=99999, predict_job_id=predict_job_id)
        predict_job.task_list = predict_task_list
        return predict_job

    @staticmethod
    def get_predict_job_list_by_nlp_task_id(nlp_task_id, doc_type_id, search, order_by, order_by_desc, offset, limit, current_user: CurrentUser):
        # if exists doc_type_id, get train jobs of this doc_type_id
        if doc_type_id:
            count, predict_job_list = PredictJobModel().get_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search,
                                                                           order_by=order_by, order_by_desc=order_by_desc,
                                                                           offset=offset, limit=limit,
                                                                           current_user=current_user, doc_type_id=doc_type_id)
        else:  # else get all
            count, predict_job_list = PredictJobModel().get_by_nlp_task_id(nlp_task_id=nlp_task_id, search=search,
                                                                           order_by=order_by, order_by_desc=order_by_desc,
                                                                           offset=offset, limit=limit, current_user=current_user)

        return count, predict_job_list

    @staticmethod
    def update_predict_job_by_id(predict_job_id, args) -> PredictJob:
        predict_job = PredictJobModel().update(predict_job_id, **args)
        session.commit()
        return predict_job

    @staticmethod
    def delete_predict_job_by_id(predict_job_id):
        PredictJobModel().delete(predict_job_id)
        session.commit()

    @staticmethod
    def create_predict_job_by_doc_type_id(doc_type_id, predict_job_name, predict_job_desc, predict_job_type, files):
        # verify doc_type
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        # create predict job
        predict_job = PredictJobModel().create(doc_type_id=doc_type_id,
                                               predict_job_name=predict_job_name,
                                               predict_job_desc=predict_job_desc,
                                               predict_job_type=predict_job_type,
                                               predict_job_status=int(StatusEnum.processing))

        pipe = r.pipeline()
        for f in files:
            if get_ext(f.filename) == 'csv': # 批量处理
                doc_unique_name, doc_relative_path = upload_fileset.save_file(f.filename, f.stream.read())
                csv_doc = DocModel().create(doc_raw_name=f.filename,
                                            doc_unique_name=doc_unique_name)
                # doc, _, doc_relative_path = self.file_processor(file)
                content_list = upload_fileset.read_csv(doc_relative_path)

                # bulk create doc
                doc_name_list = []
                for txt_content in content_list:
                    doc_unique_name, _ = upload_fileset.save_file('format.txt', txt_content)
                    doc_name_list.append(doc_unique_name)
                doc_list = [dict(doc_raw_name=csv_doc.doc_raw_name, doc_unique_name=d) for d in doc_name_list]
                doc_list = DocModel().bulk_create(doc_list)

                # bulk create predict tasks
                task_list = []
                for i in range(len(doc_list)):
                    task_list.append(dict(
                        doc_id=doc_list[i].doc_id,
                        predict_job_id=predict_job.predict_job_id,
                        predict_task_status=int(StatusEnum.processing)
                    ))
                task_list = PredictTaskModel().bulk_create(task_list)
                # push redis
                for i in range(len(doc_list)):
                    push_predict_task_to_redis(predict_job=predict_job, predict_task=task_list[i], doc=doc_list[i])

            elif get_ext(f.filename) in ['txt', 'docx', 'doc', 'pdf']: # 单文件处理
                doc_unique_name, doc_relative_path = upload_fileset.save_file(f.filename, f.stream.read())
                doc = DocModel().create(doc_raw_name=f.filename,
                                        doc_unique_name=doc_unique_name)
                predict_task = PredictTaskModel().create(doc_id=doc.doc_id,
                                                         predict_job_id=predict_job.predict_job_id,
                                                         predict_task_status=int(StatusEnum.processing))
                push_predict_task_to_redis(predict_job=predict_job, predict_task=predict_task, doc=doc)
            else:
                abort(400, message="文件类型出错")

        pipe.execute()
        session.commit()
        return predict_job


def push_predict_task_to_redis(predict_job, predict_task, doc):
    r.lpush(_get('EXTRACT_TASK_QUEUE_KEY'), json.dumps({
        'files': [
            {
                'file_name': doc.doc_unique_name,
                'is_scan': predict_job.predict_job_type == FileTypeEnum.ocr,
                'doc_id': doc.doc_id,
                'doc_type': f'NER{str(predict_job.doc_type_id)}'
            },
        ],
        'is_multi': False,
        'doc_id': doc.doc_id,
        'doc_type': f'NER{str(predict_job.doc_type_id)}',
        'business': "extract",
        'task_id': predict_task.predict_task_id,
    }))