# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-3:40 下午
from abc import ABC
from sqlalchemy import not_

from app.common.filters import CurrentUser
from app.model.base import BaseModel
from app.entity import TrainTask, TrainJob, DocType
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

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_id"]
        # Compose query
        q = session.query(TrainTask).filter(~TrainTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainTask, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(TrainTask, order_by).desc())
        else:
            q = q.order_by(getattr(TrainTask, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> TrainTask:
        entity = TrainTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def delete(self, _id):
        session.query(TrainTask).filter(TrainTask.doc_type_id == _id).update({TrainTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass

    @staticmethod
    def get_by_nlp_task_id(nlp_task_id, search, current_user: CurrentUser, order_by="created_time", order_by_desc=True,
                           limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        # Compose query
        q = session.query(TrainTask, TrainJob, DocType) \
            .join(TrainJob, TrainTask.train_job_id == TrainJob.train_job_id) \
            .join(DocType, DocType.doc_type_id == TrainJob.doc_type_id) \
            .filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~TrainJob.is_deleted)
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))

        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        if search:
            q = q.filter(TrainJob.train_job_name.like(f'%{search}%'))
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(TrainJob, order_by).desc())
        else:
            q = q.order_by(getattr(TrainJob, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()