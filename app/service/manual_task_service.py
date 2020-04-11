# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: manual_task_service.py 
@Time: 2020/04/11 14:00
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.model import MarkTaskModel, MarkJobModel, UserTaskModel
from app.common.extension import session


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
