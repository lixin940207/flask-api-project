# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: manual_task_service.py 
@Time: 2020/04/11 14:00
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.common import NlpTaskEnum, StatusEnum, RoleEnum
from app.common.filters import CurrentUser
from app.model import MarkTaskModel, MarkJobModel, UserTaskModel
from app.common.extension import session
from app.schema import MarkTaskSchema
from app.schema import UserTaskSchema

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
        if current_user.user_role in [RoleEnum.annotator.value]:
            count, processed, items = UserTaskModel().get_user_task_with_doc_and_doc_type(nlp_task_id=nlp_task_id,
                                                                                      current_user=current_user,
                                                                                      args=args)
            schema = UserTaskSchema
            task_type = 'user'
        else:
            count, processed, items = MarkTaskModel().get_mark_task_with_doc_and_doc_type(nlp_task_id=nlp_task_id,
                                                                                          current_user=current_user,
                                                                                          args=args)
            task_type = 'mark'
            schema = MarkTaskSchema
        if args['job_type'] == 'classify_mark':
            # TODO 返回数据格式转换
            result = schema(many=True).dump(items)
        else:
            result = schema(many=True, exclude=('user_task_result', 'mark_task_result')).dump(items)
        for item in result:
            item['task_id'] = item[task_type+'_task_id']
            del item[task_type + '_task_id']
            task_state = item[task_type + '_task_status']
            del item['user_task_status']
            if task_state == StatusEnum.fail:
                task_state = 'failed'
            elif task_state == StatusEnum.reviewing:
                task_state = 'unaudit'
            elif task_state == StatusEnum.approved:
                task_state = 'audited'
            else:
                task_state = StatusEnum(task_state).value
            item['task_state'] = task_state
        return count, processed, result
