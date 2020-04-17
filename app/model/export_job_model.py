from abc import ABC

from sqlalchemy import not_

from app.common.common import StatusEnum
from app.entity import DocType
from app.model.base import BaseModel
from app.entity.export_job import ExportJob
from app.common.extension import session


class ExportJobModel(BaseModel, ABC):
    def get_all(self):
        raise NotImplemented("no get_all")
        # return session.query(ExportJob).filter(not_(ExportJob.is_deleted)).all()

    def get_by_id(self, _id):
        return session.query(ExportJob).filter(ExportJob.export_job_id == _id, not_(ExportJob.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["export_job_status", "doc_type_id"]
        # Compose query
        q = session.query(ExportJob).filter(not_(ExportJob.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(ExportJob, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> ExportJob:
        entity = ExportJob(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(ExportJob).filter(ExportJob.export_job_id == _id).update({ExportJob.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(ExportJob).filter(ExportJob.export_job_id.in_(_id_list)).update({ExportJob.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        raise NotImplemented("no bulk_update")

    @staticmethod
    def get_export_history(current_user, offset, limit):
        q = session.query(ExportJob.export_job_id, ExportJob.created_time, ExportJob.export_file_path,
                          DocType.nlp_task_id, ExportJob.doc_type_id, ExportJob.export_job_status, DocType.doc_type_name) \
            .outerjoin(DocType, ExportJob.doc_type_id == DocType.doc_type_id) \
            .filter(ExportJob.created_by == current_user.user_id, ~ExportJob.is_deleted, ~DocType.is_deleted)

        count = q.count()
        q = q.order_by(ExportJob.export_job_id.desc())
        q = q.offset(offset).limit(limit)
        return q.all(), count

    @staticmethod
    def update_status(export_id, status):
        session.query(ExportJob).filter(ExportJob.export_job_id == export_id) \
            .update({ExportJob.export_job_status: StatusEnum[status].value})
        session.flush()
