# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-4:54 下午
from abc import ABC
from sqlalchemy import func as sa_func

from app.common.seeds import StatusEnum
from app.entity import TrainTask, TrainJob
from app.model.base import BaseModel
from app.entity.evaluate_task import EvaluateTask

from app.common.extension import session


class EvaluateTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(EvaluateTask).filter(~EvaluateTask.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(EvaluateTask).filter(EvaluateTask.evaluate_task_id == _id,
                                                  ~EvaluateTask.is_deleted).one()

    @staticmethod
    def is_empty_table():
        return session.query(EvaluateTask).filter(~EvaluateTask.is_deleted).count() == 0

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_task_id"]
        # Compose query
        q = session.query(EvaluateTask).filter(~EvaluateTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(EvaluateTask, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> EvaluateTask:
        entity = EvaluateTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(EvaluateTask).filter(EvaluateTask.doc_type_id == _id).update({EvaluateTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass

    @staticmethod
    def get_latest_evaluate_by_doc_type_id(nlp_task, doc_type_id):
        evaluate_result_path = '$.result.overall."f1-score"' if nlp_task == 'classify' else '$.scores.f1_score.overall.f1'
        q = session.query(EvaluateTask)\
            .join(TrainTask, TrainTask.train_task_id == EvaluateTask.train_task_id)\
            .join(TrainJob, TrainJob.train_job_id == TrainTask.train_job_id)\
            .filter(
            EvaluateTask.evaluate_task_status == StatusEnum.success,
            TrainJob.doc_type_id == doc_type_id,
            ~EvaluateTask.is_deleted,
            ~TrainTask.is_deleted,
            ~TrainJob.is_deleted
        ).order_by(
            sa_func.json_extract(EvaluateTask.evaluate_task_result, evaluate_result_path).desc())
        return q.first()
