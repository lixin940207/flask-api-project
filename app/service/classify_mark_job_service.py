# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/23
from app.common.seeds import NlpTaskEnum
from app.model import MarkJobModel, MarkTaskModel
from app.resource.v2.mark.classify_mark_job.schema import ClassifyMarkJobSchema


# class ClassifyMarkJobService:
#     @staticmethod
#     def get_mark_job_list(user_id, user_role, args):
#         nlp_task_id = int(NlpTaskEnum.classify)
#         mark_jobs = MarkJobModel().get_by_nlp_task_id(
#             nlp_task_id=nlp_task_id, doc_type_id=args['doc_type_id'],
#             search=args['query'], limit=args['limit'], offset=args['offset'])
#
#         count = MarkJobModel().count_mark_job_by_nlp_task_id(
#             nlp_task_id=nlp_task_id, search=args['query'])
#
#         mark_job_ids = [item.mark_job_id for item in mark_jobs]
#         stats = MarkTaskModel().count_mark_task_status(mark_job_ids=mark_job_ids, user_id=user_id)
#
#         for item in mark_jobs:
#             stats = get_stats_by_job_id(item.mark_job_id)
#             setattr(item, 'stats', stats)
#
#         result = ClassifyMarkJobSchema(many=True).dump(mark_jobs)
#         return count, result
