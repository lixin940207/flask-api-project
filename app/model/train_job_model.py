# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/18-2:34 下午
from abc import ABC
from sqlalchemy import not_
from app.model.base import BaseModel
from app.entity.train_job import TrainJob
from app.entity.doc_type import DocType
from app.common.extension import session
from sqlalchemy import func


class TrainJobModel(BaseModel, ABC):
    def get_all(self):
        return session.query(TrainJob).filter(not_(TrainJob.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(TrainJob).filter(TrainJob.train_job_id == _id, not_(TrainJob.is_deleted)).one()

    def get_by_filter(self, search, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        # Compose query
        q = session.query(TrainJob).filter(~TrainJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        if search:
            q = q.filter(TrainJob.train_job_name.like(f'%{search}%'))
        # Order by key, Descending or ascending order
        if order_by_desc:
            q = q.order_by(getattr(TrainJob, order_by).desc())
        else:
            q = q.order_by(getattr(TrainJob, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def get_by_nlp_task_id(self, nlp_task_id, search, order_by="created_time", order_by_desc=True, limit=0, offset=10,
                           **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        # Compose query
        q = session.query(TrainJob).join(
            DocType, DocType.doc_type_id == DocType.doc_type_id
        ).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~TrainJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        if search:
            q = q.filter(TrainJob.train_job_name.like(f'%{search}%'))
        # Order by key, Descending or ascending order
        if order_by_desc:
            q = q.order_by(getattr(TrainJob, order_by).desc())
        else:
            q = q.order_by(getattr(TrainJob, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def count_by_filter(self, search, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        # Compose query
        q = session.query(func.count(TrainJob.train_job_id)).filter(~TrainJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        if search:
            q = q.filter(TrainJob.train_job_name.like(f'%{search}%'))
        return q.one()[0]

    @staticmethod
    def count_by_nlp_task_id(nlp_task_id, search, **kwargs):
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        q = session.query(func.count(TrainJob.train_job_id)) \
            .join(DocType, TrainJob.doc_type_id == DocType.doc_type_id) \
            .filter(~TrainJob.is_deleted, ~DocType.is_deleted, DocType.nlp_task_id == nlp_task_id)
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(TrainJob, key) == val)
        if search:
            q = q.filter(TrainJob.train_job_name.like(f'%{search}%'))
        return q.one()[0]

    def create(self, **kwargs) -> TrainJob:
        entity = TrainJob(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: [TrainJob]) -> [TrainJob]:
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(TrainJob).filter(TrainJob.train_job_id == _id).update({TrainJob.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mapping
        pass

    @staticmethod
    def count_train_job_by_nlp_task(user_id):
        count = session.query(DocType.nlp_task_id, func.count(TrainJob.train_job_id)) \
            .join(DocType, TrainJob.doc_type_id == DocType.doc_type_id) \
            .filter(~TrainJob.is_deleted, ~DocType.is_delete, DocType.created_by == user_id) \
            .group_by(DocType.nlp_task_id).all()
        return count
