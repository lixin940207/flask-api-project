# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:32 下午
from abc import ABC

from sqlalchemy import distinct

from app.common.common import RoleEnum
from app.common.extension import session
from app.common.filters import CurrentUser
from app.entity import PredictTask, DocType
from app.model.base import BaseModel


class PredictTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(PredictTask).filter(~PredictTask.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(PredictTask).filter(PredictTask.predict_task_id == _id, PredictTask.is_deleted).one()

    def get_by_filter(self, search="", order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["predict_task_status", "predict_job_id"]
        # Compose query
        q = session.query(PredictTask).filter(~PredictTask.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(PredictTask, key) == val)
        if search:
            q = q.filter(PredictTask.predict_task_name.like(f'%{search}%'))
        count = q.count()
        # Order by key, Descending or ascending order
        if order_by_desc:
            q = q.order_by(getattr(PredictTask, order_by).desc())
        else:
            q = q.order_by(getattr(PredictTask, order_by))
        q = q.offset(offset).limit(limit)
        return count, q.all()

    @staticmethod
    def get_by_nlp_task_id(nlp_task_id, search, current_user: CurrentUser, order_by="created_time", order_by_desc=True,
                           limit=10, offset=0, **kwargs):
        """
        get (traintask, trainjob, doctype) tuple by nlp_task_id and other filters
        """
        # Define allowed filter keys
        accept_keys = ["train_job_status", "doc_type_id"]
        # Compose query, select 3 tables related to a train job
        q = session.query(PredictTask, PredictJob, DocType) \
            .join(PredictTask, PredictTask.predict_job_id == PredictJob.predict_job_id) \
            .join(DocType, DocType.doc_type_id == PredictJob.doc_type_id) \
            .filter(DocType.nlp_task_id == nlp_task_id,
                    ~DocType.is_deleted,
                    ~PredictJob.is_deleted,
                    ~PredictTask.is_deleted)
        # auth
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(PredictJob, key) == val)
        if search:
            q = q.filter(PredictJob.predict_job_name.like(f'%{search}%'))
        count = q.with_entities(distinct(PredictJob.predict_job_id)).count()
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(PredictJob, order_by).desc())
        else:
            q = q.order_by(getattr(PredictJob, order_by))
        q = q.offset(offset).limit(limit)
        return count, q.all()

    def create(self, **kwargs) -> PredictTask:
        entity = PredictTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: [PredictTask]) -> [PredictTask]:
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(PredictTask).filter(PredictTask.predict_task_id == _id).update({PredictTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mapping
        pass