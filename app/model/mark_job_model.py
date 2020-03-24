from abc import ABC

from sqlalchemy import not_, func
from app.model.base import BaseModel
from app.entity import MarkJob, DocType, UserTask, MarkTask
from app.common.extension import session
from app.common.seeds import StatusEnum


class MarkJobModel(BaseModel, ABC):
    def get_all(self):
        return session.query(MarkJob).filter(MarkJob.is_deleted == False).all()

    def get_by_id(self, _id):
        return session.query(MarkJob).filter(MarkJob.mark_job_id == _id, not_(MarkJob.is_deleted)).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(MarkJob).filter(not_(MarkJob.is_deleted))
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkJob, key) == val)
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def get_by_nlp_task_id(
            self, nlp_task_id, search, order_by="created_time", order_by_desc=True, limit=0, offset=10, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(MarkJob).join(
            DocType, DocType.doc_type_id == DocType.doc_type_id
        ).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~MarkJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkJob, key) == val)
        if search:
            q = q.filter(MarkJob.mark_job_name.like(f'%{search}%'))
        # Order by key
        q = q.order_by(order_by)
        # Descending order
        if order_by_desc:
            q = q.desc()
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, entity):
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: [MarkJob]) -> [MarkJob]:
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(MarkJob).filter(MarkJob.mark_job_id == _id).update({MarkJob.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(MarkJob).filter(MarkJob.mark_job_id.in_(_id_list)).update({MarkJob.is_deleted: True})
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        raise NotImplemented("no bulk_update")
        pass

    @staticmethod
    def count_mark_job_by_nlp_task_id(nlp_task_id, search, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(func.count(MarkJob.mark_job_id)).join(
            DocType, DocType.doc_type_id == DocType.doc_type_id
        ).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~MarkJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkJob, key) == val)
        if search:
            q = q.filter(MarkJob.mark_job_name.like(f'%{search}%'))
        return q.one()[0]

    @staticmethod
    def count_mark_job_by_nlp_task_manager(user_id):
        all_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by == user_id) \
            .group_by(DocType.nlp_task_id).all()
        labeled_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by == user_id,
                    MarkJob.mark_job_status.in_([int(StatusEnum.labeled), int(StatusEnum.reviewing),
                                                 int(StatusEnum.approved)])) \
            .group_by(DocType.nlp_task_id).all()
        reviewed_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(MarkJob.is_deleted == False, DocType.is_deleted == False, DocType.created_by == user_id,
                    MarkJob.mark_job_status.in_([int(StatusEnum.approved)])) \
            .group_by(DocType.nlp_task_id).all()
        return all_count, labeled_count, reviewed_count

    @staticmethod
    def count_mark_job_by_nlp_task_reviewer(user_id):
        all_count = session.query(func.count(MarkJob.mark_job_status), DocType.nlp_task_id, DocType.doc_type_id, MarkJob.mark_job_status) \
            .join(MarkTask, MarkTask.mark_job_id == MarkJob.mark_job_id) \
            .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
            .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
            .filter(not_(UserTask.is_deleted), not_(MarkTask.is_deleted), not_(MarkJob.is_deleted),
                    not_(DocType.is_deleted), UserTask.annotator_id == user_id) \
            .group_by(MarkJob.mark_job_status, MarkJob.doc_type_id, DocType.nlp_task_id).all()

        # all_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
        #     .join(MarkTask, MarkTask.mark_job_id == MarkJob.mark_job_id) \
        #     .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
        #     .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
        #     .filter(not_(UserTask.is_deleted), not_(MarkTask.is_deleted), not_(MarkJob.is_deleted),
        #             not_(DocType.is_deleted), UserTask.annotator_id == user_id) \
        #     .group_by(DocType.nlp_task_id).all()
        # labeled_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
        #     .join(MarkTask, MarkTask.mark_job_id == MarkJob.mark_job_id) \
        #     .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
        #     .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
        #     .filter(not_(UserTask.is_deleted), not_(MarkTask.is_deleted), not_(MarkJob.is_deleted),
        #             not_(DocType.is_deleted), UserTask.annotator_id == user_id,
        #             MarkJob.mark_job_status.in_([int(StatusEnum.labeled), int(StatusEnum.reviewing),
        #                                          int(StatusEnum.approved)])) \
        #     .group_by(DocType.nlp_task_id).all()
        # reviewed_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
        #     .join(MarkTask, MarkTask.mark_job_id == MarkJob.mark_job_id) \
        #     .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
        #     .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
        #     .filter(not_(UserTask.is_deleted), not_(MarkTask.is_deleted), not_(MarkJob.is_deleted),
        #             not_(DocType.is_deleted), UserTask.annotator_id == user_id,
        #             MarkJob.mark_job_status.in_([int(StatusEnum.approved)])) \
        #     .group_by(DocType.nlp_task_id).all()
        return all_count
