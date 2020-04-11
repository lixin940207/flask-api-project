# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:32 下午
from abc import ABC

from sqlalchemy import distinct

from app.common.common import RoleEnum
from app.common.extension import session
from app.common.filters import CurrentUser
from app.entity import PredictTask, DocType, Doc
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
    def get_predict_task_and_doc(predict_job_id):
        q = session.query(PredictTask, Doc) \
            .join(Doc, Doc.doc_id == PredictTask.doc_id) \
            .filer(
            PredictTask.predict_job_id == predict_job_id,
            ~Doc.is_deleted,
            ~PredictTask.is_deleted,
            )
        return q.all()

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
        session.query(PredictTask).filter(PredictTask.predict_task_id == _id).update({PredictTask.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mapping
        pass