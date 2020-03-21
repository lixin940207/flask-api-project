# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
from abc import ABC

from app.model.base import BaseModel
from app.entity import MarkJob, DocType
from app.common.extension import session
from sqlalchemy import func
from app.common.seeds import StatusEnum


class MarkJobModel(BaseModel, ABC):
    def get_all(self):
        return session.query(MarkJob).filter(MarkJob.is_deleted == False).all()

    def get_by_id(self, _id):
        pass

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        pass

    def create(self, entity: MarkJob) -> MarkJob:
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: [MarkJob]) -> [MarkJob]:
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        pass

    def bulk_delete(self, _id_list):
        pass

    def update(self, entity):
        # session.bulk_update_mappings
        pass

    def bulk_update(self, entity_list):
        pass

    @staticmethod
    def count_mark_job_by_nlp_task(user_id):
        all_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by==user_id) \
            .group_by(DocType.nlp_task_id).all()
        labeled_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by==user_id,
                    MarkJob.mark_job_status.in_([int(StatusEnum.labeled), int(StatusEnum.reviewing),
                                                int(StatusEnum.approved)])) \
            .group_by(DocType.nlp_task_id).all()
        reviewed_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by==user_id,
                    MarkJob.mark_job_status.in_([int(StatusEnum.approved)])) \
            .group_by(DocType.nlp_task_id).all()
        return all_count, labeled_count, reviewed_count
