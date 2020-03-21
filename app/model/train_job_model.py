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

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_type_id", "nlp_task_id"]
        # Compose query
        q = session.query(TrainJob).filter(not_(TrainJob.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                if key == "doc_type_id":
                    q = q.filter(TrainJob.doc_type_id == val)
                elif key == 'nlp_task_id':
                    q = q.join(DocType, DocType.doc_type_id == TrainJob.doc_type_id).filter(not_(DocType.is_deleted),
                                                                                            DocType.nlp_task_id == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity: TrainJob) -> TrainJob:
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
            .filter(TrainJob.is_deleted==False, DocType.is_deleted==False, DocType.created_by==user_id) \
            .group_by(DocType.nlp_task_id).all()
        return count
