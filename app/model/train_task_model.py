# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-3:40 下午
from abc import ABC
from sqlalchemy import not_

from app.common.filters import CurrentUser
from app.model.base import BaseModel
from app.entity import TrainTask, TrainJob, DocType, EvaluateTask
from app.common.common import StatusEnum, NlpTaskEnum, RoleEnum

from app.common.extension import session


class TrainTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainTask).filter(~TrainTask.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(TrainTask).filter(TrainTask.train_task_id == _id, ~TrainTask.is_deleted).one()

    @staticmethod
    def is_empty_table():
        return session.query(TrainTask).filter(not_(TrainTask.is_deleted)).count() == 0

    def get_by_filter(self, search="", order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_id", "model_version"]
        # Compose query
        q = session.query(TrainTask).filter(~TrainTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTask, key) == val)
        if search:
            q = q.filter(TrainTask.train_model_name.like(f'%{search}%'))
        count = q.count()
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(TrainTask, order_by).desc())
        else:
            q = q.order_by(getattr(TrainTask, order_by))
        q = q.offset(offset).limit(limit)
        return count, q.all()

    def get_by_doc_type_id(self, doc_type_id, **kwargs):
        accept_keys = ["train_status"]
        q = session.query(TrainTask)\
            .join(TrainJob, TrainJob.train_job_id == TrainTask.train_job_id)\
            .filter(TrainJob.doc_type_id == doc_type_id, ~TrainJob.is_deleted, ~TrainTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTask, key) == val)
        return q.all()

    def create(self, **kwargs) -> TrainTask:
        entity = TrainTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(TrainTask).filter(TrainTask.train_task_id == _id).update({TrainTask.is_deleted: True})
        session.flush()

    def update(self, _id, **kwargs):
        entity = session.query(TrainTask).filter(TrainTask.train_task_id == _id)
        entity.update(**kwargs)
        session.flush()
        return entity

    @staticmethod
    def get_all_model_related_by_doc_type_id(doc_type_id, current_user: CurrentUser, order_by="created_time", order_by_desc=True, offset=0, limit=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status"]
        # Compose query
        q = session.query(TrainTask, EvaluateTask, TrainJob, DocType) \
            .join(EvaluateTask, EvaluateTask.train_task_id == TrainTask.train_task_id) \
            .join(TrainJob, TrainTask.train_job_id == TrainJob.train_job_id) \
            .join(DocType, DocType.doc_type_id == TrainJob.doc_type_id) \
            .filter(DocType.doc_type_id == doc_type_id,
                    TrainTask.train_status == int(StatusEnum.online),
                    EvaluateTask.evaluate_task_status == int(StatusEnum.success),
                    ~DocType.is_deleted,
                    ~TrainJob.is_deleted,
                    ~TrainTask.is_deleted,
                    ~EvaluateTask.is_deleted)
        # auth
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))

        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(TrainJob, order_by).desc())
        else:
            q = q.order_by(getattr(TrainJob, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()
