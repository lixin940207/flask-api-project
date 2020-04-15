# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-4:54 下午
from abc import ABC
from sqlalchemy import func as sa_func

from app.common.common import NlpTaskEnum
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
        if order_by_desc:
            q = q.order_by(getattr(EvaluateTask, order_by).desc())
        else:
            q = q.order_by(getattr(EvaluateTask, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    @staticmethod
    def get_by_train_job_id(train_job_id, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        accept_keys = ["train_task_id", "evaluate_task_status"]
        # Compose query
        q = session.query(EvaluateTask)\
            .join(TrainTask, TrainTask.train_task_id == EvaluateTask.train_task_id)\
            .filter(TrainTask.train_job_id == train_job_id, ~EvaluateTask.is_deleted, ~TrainTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(EvaluateTask, key) == val)
        # count
        count = q.count()
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(EvaluateTask, order_by).desc())
        else:
            q = q.order_by(getattr(EvaluateTask, order_by))
        q = q.offset(offset).limit(limit)
        return count, q.all()

    def create(self, **kwargs) -> EvaluateTask:
        entity = EvaluateTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(EvaluateTask).filter(EvaluateTask.evaluate_task_id == _id).update({EvaluateTask.is_deleted: True})
        session.flush()

    def update(self, _id, **kwargs):
        entity = session.query(EvaluateTask).filter(EvaluateTask.evaluate_task_id == _id)
        entity.update(kwargs)
        session.flush()
        return entity.one()

    @staticmethod
    def get_latest_evaluate_by_doc_type_id(nlp_task_id, doc_type_id):
        evaluate_result_path = '$.result.overall."f1-score"' if nlp_task_id == int(NlpTaskEnum.classify) else '$.scores.f1_score.overall.f1'
        q = session.query(EvaluateTask)\
            .join(TrainTask, TrainTask.train_task_id == EvaluateTask.train_task_id)\
            .join(TrainJob, TrainJob.train_job_id == TrainTask.train_job_id)\
            .filter(
            EvaluateTask.evaluate_task_status == int(StatusEnum.success),
            TrainJob.doc_type_id == doc_type_id,
            ~EvaluateTask.is_deleted,
            ~TrainTask.is_deleted,
            ~TrainJob.is_deleted
        ).order_by(
            sa_func.json_extract(EvaluateTask.evaluate_task_result, evaluate_result_path).desc())
        return q.first()
