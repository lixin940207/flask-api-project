# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: manual_task_service.py 
@Time: 2020/04/11 14:00
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.common import NlpTaskEnum, StatusEnum
from app.common.filters import CurrentUser
from app.model import MarkTaskModel, MarkJobModel, UserTaskModel
from app.common.extension import session
from app.schema.user_task_schema import UserTaskSchema

nlp_task_mapper = {
    "mark": int(NlpTaskEnum.extract),
    "classify_mark": int(NlpTaskEnum.classify),
    "relation_mark": int(NlpTaskEnum.relation),
    "wordseg_mark": int(NlpTaskEnum.wordseg),
    "extract": int(NlpTaskEnum.extract),
    "classify_extract": int(NlpTaskEnum.classify),
    "relation_extract": int(NlpTaskEnum.relation),
    "wordseg_extract": int(NlpTaskEnum.wordseg),
}


class ManualTaskService:
    @staticmethod
    def detele_task(task_id):
        mark_job_id = MarkTaskModel().get_mark_job_id_by_id(task_id)
        MarkTaskModel().delete(task_id)
        session.commit()
        mark_job_status = MarkJobModel().check_mark_job_status(mark_job_id)
        mark_job = MarkJobModel().update(mark_job_id, **{'mark_job_status': mark_job_status})
        session.commit()
        return mark_job

    @staticmethod
    def reject_manual_task(mark_task_id):
        UserTaskModel().update_status_to_unlabel_by_manual_task_id(mark_task_id)
        MarkTaskModel().update_status_to_unlabel_by_manual_task_id(mark_task_id)
        session.commit()

    @staticmethod
    def get_user_task_result(current_user: CurrentUser, args):
        nlp_task_id = nlp_task_mapper.get(args['job_type'])
        count, processed, items = UserTaskModel().get_user_task_with_doc_and_doc_type(nlp_task_id=nlp_task_id,
                                                                                      current_user=current_user,
                                                                                      args=args)
        if args['job_type'] == 'classify_mark':
            # TODO 返回数据格式转换
            result = UserTaskSchema(many=True).dump(items)
        else:
            result = UserTaskSchema(many=True, exclude=('user_task_result',)).dump(items)
        for item in result:
            item['task_id'] = item['user_task_id']
            del item['user_task_id']
            user_task_status = item['user_task_status']
            del item['user_task_status']
            if user_task_status == StatusEnum.fail:
                user_task_status = 'failed'
            elif user_task_status == StatusEnum.reviewing:
                user_task_status = 'unaudit'
            elif user_task_status == StatusEnum.approved:
                user_task_status = 'audited'
            else:
                user_task_status = StatusEnum(user_task_status).value
            item['task_state'] = user_task_status
        return count, processed, result
