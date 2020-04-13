# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-1:43 下午
from datetime import datetime

from app.common.common import StatusEnum
from app.common.extension import session
from app.common.filters import CurrentUser
from app.entity import PredictTask
from app.model import PredictJobModel, PredictTaskModel


class TaskMachineService:
    @staticmethod
    def get_predict_task_by_id(predict_task_id):
        predict_task, doc = PredictTaskModel().get_predict_task_and_doc(predict_task_id=predict_task_id)[0]
        predict_task.doc = doc
        return predict_task

    @staticmethod
    def get_predict_task_list_by_predict_job_id(predict_job_id, search, order_by, order_by_desc, offset, limit, current_user: CurrentUser, args):
        count, predict_task_list = PredictTaskModel().get_by_predict_job_id(predict_job_id=predict_job_id, search=search, order_by=order_by,
                                                 order_by_desc=order_by_desc, offset=offset, limit=limit, current_user=current_user, **args)
        return count, predict_task_list

    @staticmethod
    def update_predict_task_by_id(predict_task_id, args):
        predict_task = PredictTaskModel().update(predict_task_id, **args)
        session.commit()
        return predict_task

    @staticmethod
    def update_predict_job_status_by_predict_task(predict_task: PredictTask):
        # 更新这个task对应的job的状态，如果其下所有的task都成功，则修改job状态成功；如果其下有一个任务失败，则修改job状态失败
        _, predict_task_list = PredictTaskModel().get_by_filter(limit=99999, predict_job_id=predict_task.predict_job_id)
        states = [predict_task.predict_task_status for predict_task in predict_task_list]
        if int(StatusEnum.fail) in states:  # 有一个失败，则整个job失败
            new_job_status = int(StatusEnum.fail)
        elif int(StatusEnum.processing) in states:  # 没有失败但是有处理中，则整个job处理中
            new_job_status = int(StatusEnum.processing)
        else:
            new_job_status = int(StatusEnum.success)
        PredictJobModel().update(predict_task.predict_job_id, predict_job_status=new_job_status,
                                                              updated_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        session.commit()

    @staticmethod
    def delete_predict_task_by_id(predict_task_id):
        predict_task = PredictTaskModel().delete(predict_task_id)
        session.commit()
        return predict_task
