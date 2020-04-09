# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
from app.common.seeds import NlpTaskEnum, StatusEnum
from app.model import MarkJobModel, MarkTaskModel
from app.resource.v2.mark.classify_mark_job.schema import ClassifyMarkJobSchema


class ClassifyMarkJobService:
    @staticmethod
    def get_mark_job_list(args):
        nlp_task_id = int(NlpTaskEnum.classify)
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

        result = ClassifyMarkJobSchema(many=True).dump(items)
        return count, result
