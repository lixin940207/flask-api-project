# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:32 下午
from abc import ABC

from sqlalchemy import distinct

from app.common.common import RoleEnum
from app.common.extension import session
from app.common.filters import CurrentUser
from app.entity import PredictTask, DocType, Doc, PredictJob
from app.model.base import BaseModel


class PredictTaskModel(BaseModel, ABC):
    def get_all(self):
        return session.query(PredictTask).filter(~PredictTask.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(PredictTask).filter(PredictTask.predict_task_id == _id, PredictTask.is_deleted).one()

    def get_by_filter(self, search="", order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
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
    def get_predict_task_and_doc(**kwargs):
        accept_keys = ["predict_task_id", "predict_job_id"]
        q = session.query(PredictTask, Doc) \
            .join(Doc, Doc.doc_id == PredictTask.doc_id) \
            .filter(
            ~Doc.is_deleted,
            ~PredictTask.is_deleted,
            )
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(PredictTask, key) == val)
        return q.all()

    @staticmethod
    def get_by_predict_job_id(predict_job_id, current_user: CurrentUser, search="", order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        """
        get (traintask, trainjob, doctype) tuple by nlp_task_id and other filters
        """
        # Define allowed filter keys
        accept_keys = ["predict_task_status", "doc_type_id"]
        # Compose query, select 3 tables related to a train job
        q = session.query(PredictTask, Doc, DocType) \
            .join(PredictJob, PredictJob.predict_job_id == PredictTask.predict_job_id)\
            .join(DocType,  PredictJob.doc_type_id == DocType.doc_type_id)\
            .join(Doc, Doc.doc_id == PredictTask.doc_id) \
            .filter(PredictTask.predict_job_id == predict_job_id,
                    ~DocType.is_deleted,
                    ~Doc.is_deleted,
                    ~PredictTask.is_deleted,
                    ~PredictJob.is_deleted)
        # auth
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(PredictTask, key) == val)
        if search:
            q = q.filter(PredictTask.predict_task_name.like(f'%{search}%'))
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(PredictTask, order_by).desc())
        else:
            q = q.order_by(getattr(PredictTask, order_by))

        # assign doc_type, train_list to each trainjob for dumping
        predict_task_list = []
        for predict_task, doc, doc_type in q.all():
            # assign doc, doc_type to predict_job
            predict_task.doc_type = doc_type
            predict_task.doc = doc
            predict_task_list.append(predict_task)

        count = len(predict_task_list)
        return count, predict_task_list[offset: offset + limit]

    def create(self, **kwargs) -> PredictTask:
        entity = PredictTask(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list) -> [PredictTask]:
        entity_list = [PredictTask(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        entity = session.query(PredictTask).filter(PredictTask.predict_task_id == _id)
        entity.update({PredictTask.is_deleted: True})
        session.flush()
        return entity.one()

    def update(self, _id, **kwargs):
        entity = session.query(PredictTask).filter(PredictTask.predict_task_id == _id)
        entity.update(kwargs)
        session.flush()
        return entity.one()