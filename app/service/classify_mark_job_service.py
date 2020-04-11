# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
import json
import math
from typing import List

import pandas as pd
from pandas.errors import EmptyDataError
from werkzeug.datastructures import FileStorage

from app.common.extension import session
from app.common.fileset import upload_fileset
from app.common.redis import r
from app.common.seeds import NlpTaskEnum, StatusEnum
from app.common.utils.name import get_ext
from app.config.config import get_config_from_app as _get
from app.entity import MarkJob, MarkTask, DocType
from app.entity.base import FileTypeEnum
from app.model import MarkJobModel, MarkTaskModel, UserTaskModel, DocModel, DocTypeModel, DocTermModel
from app.schema.mark_job_schema import MarkJobSchema


class MarkJobService:
    @staticmethod
    def get_mark_job_list_by_nlp_task(args, nlp_task: NlpTaskEnum):
        nlp_task_id = int(nlp_task)
        count, result = MarkJobModel().get_by_nlp_task_id(
            nlp_task_id=nlp_task_id, doc_type_id=args['doc_type_id'],
            search=args['query'], limit=args['limit'], offset=args['offset'])

        mark_job_ids = [mark_job.mark_job_id for mark_job, _ in result]
        status_count = MarkTaskModel().count_mark_task_status(mark_job_ids=mark_job_ids)
        cache = {}
        for task_status_count, task_status, mark_job_id in status_count:
            if not cache.get(mark_job_id):
                cache[mark_job_id] = {'all': 0, 'labeled': 0, 'audited': 0}

            cache[mark_job_id]['all'] += task_status_count
            if StatusEnum.labeled <= task_status <= StatusEnum.approved:
                cache[mark_job_id]['labeled'] += task_status_count
            if task_status == StatusEnum.approved:
                cache[mark_job_id]['audited'] += task_status_count
        items = []
        for mark_job, doc_type in result:
            mark_job.stats = cache.get(mark_job.mark_job_id, {'all': 0, 'labeled': 0, 'audited': 0})
            mark_job.doc_type = doc_type
            items.append(mark_job)

        result = MarkJobSchema(many=True).dump(items)
        return count, result

    def create_mark_job(self, files, nlp_task: NlpTaskEnum, args):
        reviewer_ids = [args['assessor_id']] if args.get('assessor_id') else []
        mark_job = MarkJobModel().create(
            mark_job_name=args['mark_job_name'],
            mark_job_type=args['mark_job_type'],
            mark_job_desc=args.get('mark_job_desc'),
            doc_type_id=args['doc_type_id'],
            assign_mode=args['assign_mode'],
            reviewer_ids=reviewer_ids,
            annotator_ids=args['labeler_ids']
        )

        unassigned_tasks = []
        pipe = r.pipeline()
        for f in files:
            filename = f.filename
            if get_ext(filename) == 'csv':
                tasks = self.upload_batch_files(f, mark_job, nlp_task)
            elif get_ext(filename) in ['txt', 'docx', 'doc', 'pdf']:
                tasks = self.upload_single_file(f, mark_job, nlp_task)
            else:
                raise TypeError('file type illegal')
            for task in tasks:
                unassigned_tasks.append(task)

        if unassigned_tasks:
            # 分配标注员
            self.assign_annotator(unassigned_tasks, args['assign_mode'], args['labeler_ids'])

        pipe.execute()
        session.commit()
        result = MarkJobSchema().dump(mark_job)
        return result

    def import_mark_job(self, files, args):
        DocTypeModel().get_by_id(args['doc_type_id'])

        job = MarkJobModel().create(
            mark_job_name=args['mark_job_name'],
            mark_job_type=args['mark_job_type'],
            mark_job_desc=args.get('mark_job_desc'),
            doc_type_id=args['doc_type_id'],
            mark_job_status=int(StatusEnum.success),
            assign_mode='average',
        )
        tasks = []
        for f in files:
            single_file_tasks = self.import_labeled_files(f, args['doc_type_id'], job.mark_job_id)
            tasks.extend(single_file_tasks)
        session.commit()
        result = MarkJobSchema().dump(job)
        return result

    @staticmethod
    def delete_mark_job(mark_job_id: int):
        session.query(MarkJob).filter(MarkJob.mark_job_id == mark_job_id).update({MarkJob.is_deleted: True})
        session.query(MarkTask).filter(MarkTask.mark_job_id == mark_job_id).update({MarkTask.is_deleted: True})
        session.commit()

    @staticmethod
    def delete_mark_jobs(mark_job_ids: List[int]):
        session.query(MarkJob).filter(
            MarkJob.mark_job_id.in_(mark_job_ids)
        ).update({MarkJob.is_deleted: True}, synchronize_session='fetch')
        session.query(MarkTask).filter(
            MarkTask.mark_job_id.in_(mark_job_ids)
        ).update({MarkTask.is_deleted: True}, synchronize_session='fetch')
        session.commit()

    def upload_batch_files(self, f: FileStorage, mark_job: MarkJob, nlp_task) -> List[MarkTask]:
        doc_unique_name, doc_relative_path = upload_fileset.save_file(f.filename, f.stream.read())
        csv_doc = DocModel().create(doc_raw_name=f.filename, doc_unique_name=doc_unique_name)
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
            task_list.append(dict(doc_id=doc_list[i].doc_id, mark_job_id=mark_job.mark_job_id))
        task_list = MarkTaskModel().bulk_create(task_list)

        # push redis
        for i in range(len(doc_list)):
            self.push_mark_task_message(
                mark_job=mark_job, mark_task=task_list[i], doc=doc_list[i], business=f"{nlp_task.name}_label")

        return task_list

    def upload_single_file(self, f: FileStorage, mark_job: MarkJob, nlp_task) -> List[MarkTask]:
        doc_unique_name, doc_relative_path = upload_fileset.save_file(f.filename, f.stream.read())
        doc = DocModel().create(doc_raw_name=f.filename, doc_unique_name=doc_unique_name)
        mark_task = MarkTaskModel().create(doc_id=doc.doc_id, mark_job_id=mark_job.mark_job_id)
        self.push_mark_task_message(
            mark_job=mark_job, mark_task=mark_task, doc=doc, business=f"{nlp_task.name}_label")

        return [mark_task]

    @staticmethod
    def import_labeled_files(f, doc_type_id, mark_job_id):
        doc_unique_name, doc_relative_path = upload_fileset.save_file(f.filename, f.stream.read())
        csv_doc = DocModel().create(doc_raw_name=f.filename, doc_unique_name=doc_unique_name)
        try:
            df = pd.read_csv(doc_relative_path, skiprows=0, na_values='')
        except EmptyDataError:
            raise EmptyDataError('上传数据为空,请检查上传数据:{}'.format(f.filename))
        except Exception:
            raise EmptyDataError('上传数据处理异常,请检查上传数据:{}'.format(f.filename))
        if 'text' not in df.columns or 'label' not in df.columns:
            raise KeyError
        doc_terms = DocTermModel.get_doc_term_by_doctype(doc_type_id, offset=0, limit=9999)
        doc_term_name2id_map = {m.doc_term_name: m.doc_term_id for m in doc_terms}
        content_list = []
        task_results = []
        for row_num, row in df.iterrows():
            content = row.get('text')
            label = row.get('label')
            try:
                label_id = doc_term_name2id_map[label]
            except KeyError as ke:
                raise ValueError(f"当前项目不存在文件第{row_num + 2}行的label:{ke.args[0]}，请检查")
            task_result = [{'prob': 1, 'marked': 1, 'label_id': label_id, 'label_name': label}]
            if content and label:
                content_list.append(content)
                task_results.append(task_result)

        # bulk insert doc
        unique_name_list = []
        for txt_content in content_list:
            doc_unique_name, _ = upload_fileset.save_file('format.txt', txt_content)
            unique_name_list.append(doc_unique_name)
        doc_list = [
            dict(
                doc_raw_name=csv_doc.doc_raw_name,
                doc_unique_name=unique_name,
                origin_file_name=csv_doc.doc_unique_name
            ) for unique_name in unique_name_list
        ]
        doc_entity_list = DocModel().bulk_create(doc_list)

        # bulk insert task
        task_list = []
        for i in range(len(doc_list)):
            task_list.append(dict(
                doc_id=doc_entity_list[i].doc_id,
                mark_job_id=mark_job_id,
                mark_task_result=task_results[i] if task_results else {},
                mark_task_status=StatusEnum.approved
            ))
        task_entity_list = MarkTaskModel().bulk_create(task_list)

        return task_entity_list

    @staticmethod
    def push_mark_task_message(mark_job, mark_task, doc, business):
        r.lpush(_get('EXTRACT_TASK_QUEUE_KEY'), json.dumps({
            'files': [
                {
                    'file_name': doc.doc_unique_name,
                    'is_scan': mark_job.mark_job_type == FileTypeEnum.ocr,
                    'doc_id': doc.doc_id,
                    'doc_type': mark_job.doc_type_id,
                },
            ],
            'is_multi': False,
            'doc_id': doc.doc_id,
            'doc_type': mark_job.doc_type_id,
            'business': business,
            'task_id': mark_task.mark_task_id,
        }))

    @staticmethod
    def assign_annotator(task_list: List, mode: str, annotator_ids: List[int]) -> None:
        if mode == 'average':
            # 均分标注
            step = math.ceil(len(task_list) / len(annotator_ids))
            nest_list = [task_list[i:i + step] for i in range(0, len(task_list), step)]

            for index, annotator_id in enumerate(annotator_ids[:len(nest_list)]):
                for task in nest_list[index]:
                    UserTaskModel().create(mark_task_id=task.mark_task_id, annotator_id=annotator_id)

        if mode == 'together':
            # 分别标注
            for annotator_id in annotator_ids:
                for task in task_list:
                    UserTaskModel().create(mark_task_id=task.mark_task_id, annotator_id=annotator_id)
