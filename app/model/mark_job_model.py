from abc import ABC

from sqlalchemy import not_, func, or_, text
from typing import List
from app.common.filters import CurrentUser
from app.model.base import BaseModel
from app.entity import MarkJob, DocType, UserTask, MarkTask
from app.common.extension import session
from app.common.common import StatusEnum, RoleEnum


class MarkJobModel(BaseModel, ABC):
    def get_all(self):
        return session.query(MarkJob).filter(~MarkJob.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(MarkJob).filter(MarkJob.mark_job_id == _id, ~MarkJob.is_deleted).one()

    def get_by_ids(self, ids):
        return session.query(MarkJob).filter(MarkJob.mark_job_id.in_(ids), ~MarkJob.is_deleted).all()

    def get_by_mark_job_ids(self, mark_job_ids):
        return session.query(MarkTask).filter(MarkTask.mark_job_id.in_(mark_job_ids), ~MarkTask.is_deleted).all()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(MarkJob).filter(~MarkJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(MarkJob, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(MarkJob, order_by).desc())
        else:
            q = q.order_by(getattr(MarkJob, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def get_by_nlp_task_id(
            self, nlp_task_id, search, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(MarkJob, DocType).join(
            DocType, MarkJob.doc_type_id == DocType.doc_type_id
        ).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted, ~MarkJob.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys and val is not None:
                q = q.filter(getattr(MarkJob, key) == val)
        if search:
            q = q.filter(MarkJob.mark_job_name.like(f'%{search}%'))
        count = q.count()
        # Order by key
        q = q.order_by(text(f"{'-' if order_by_desc else ''}mark_job.{order_by}"))
        q = q.offset(offset).limit(limit)
        return count, q.all()

    def get_by_mark_job_id_list(self, mark_job_id_list) -> List[MarkJob]:
        # Compose query
        q = session.query(MarkJob).filter(~MarkJob.is_deleted,
                                          MarkJob.mark_job_id.in_(mark_job_id_list))
        return q.all()

    def create(self, **kwargs):
        entity = MarkJob(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list: List[MarkJob]) -> List[MarkJob]:
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(MarkJob).filter(MarkJob.mark_job_id == _id).update({MarkJob.is_deleted: True})
        session.query(MarkTask).filter(MarkTask.mark_job_id == _id).update({MarkTask.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(MarkJob).filter(
            MarkJob.mark_job_id.in_(_id_list)).update({MarkJob.is_deleted: True}, synchronize_session='fetch')
        session.query(MarkTask).filter(
            MarkTask.mark_job_id.in_(_id_list)).update({MarkTask.is_deleted: True}, synchronize_session='fetch')
        session.flush()

    def bulk_delete_by_filter(self, **kwargs):
        raise NotImplemented("no bulk_delete_by_filter")

    def update(self, _id, **kwargs):
        entity = session.query(MarkJob).filter(MarkJob.mark_job_id == _id)
        entity.update(kwargs)
        session.flush()
        return entity.one()

    def bulk_update(self, entity_list):
        raise NotImplemented("no bulk_update")

    @staticmethod
    def count_mark_job_by_nlp_task_id(nlp_task_id, search, **kwargs):
        # Define allowed filter keys
        accept_keys = ["assign_mode", "mark_job_status", "mark_job_type", "doc_type_id"]
        # Compose query
        q = session.query(func.count(MarkJob.mark_job_id)).join(
            DocType, MarkJob.doc_type_id == DocType.doc_type_id
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
            .filter(~MarkJob.is_deleted, ~DocType.is_deleted, DocType.created_by == user_id) \
            .group_by(DocType.nlp_task_id).all()
        labeled_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(~MarkJob.is_deleted, ~DocType.is_deleted, DocType.created_by == user_id,
                    MarkJob.mark_job_status.in_([StatusEnum.labeled, StatusEnum.reviewing, StatusEnum.approved])) \
            .group_by(DocType.nlp_task_id).all()
        reviewed_count = session.query(DocType.nlp_task_id, func.count(MarkJob.mark_job_id)) \
            .join(DocType, MarkJob.doc_type_id == DocType.doc_type_id) \
            .filter(~MarkJob.is_deleted, ~DocType.is_deleted, DocType.created_by == user_id,
                    MarkJob.mark_job_status.in_([StatusEnum.approved])) \
            .group_by(DocType.nlp_task_id).all()
        return all_count, labeled_count, reviewed_count

    @staticmethod
    def count_mark_job_by_nlp_task(current_user: CurrentUser):
        q = session.query(func.count(MarkJob.mark_job_status), DocType.nlp_task_id, DocType.doc_type_id,
                          MarkJob.mark_job_status)
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups)).filter(~DocType.is_deleted,
                                                                                ~UserTask.is_deleted,
                                                                                ~MarkTask.is_deleted,
                                                                                ~MarkJob.is_deleted)
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            q = q.join(MarkTask, MarkTask.mark_job_id == MarkJob.mark_job_id) \
                .join(UserTask, UserTask.mark_task_id == MarkTask.mark_task_id) \
                .join(DocType, DocType.doc_type_id == MarkJob.doc_type_id) \
                .filter(~DocType.is_deleted, ~UserTask.is_deleted, ~MarkTask.is_deleted, ~MarkJob.is_deleted) \
                .filter(
                or_(UserTask.annotator_id == current_user.user_id, UserTask.annotator_id == current_user.user_id))
        all_count = q.group_by(MarkJob.mark_job_status, MarkJob.doc_type_id, DocType.nlp_task_id, DocType.doc_type_id).all()
        return all_count

    @staticmethod
    def check_mark_job_status(mark_job_id):
        q = session.query(MarkTask).filter(
            MarkTask.mark_job_id == mark_job_id,
            ~MarkTask.is_deleted
        ).all()
        states = [item.mark_task_status for item in q]
        if int(StatusEnum.init) in states:
            mark_job_status = int(StatusEnum.processing)
        elif int(StatusEnum.fail) in states:
            mark_job_status = int(StatusEnum.fail)
        elif int(StatusEnum.processing) in states:
            mark_job_status = int(StatusEnum.processing)
        elif int(StatusEnum.labeling) in states or int(StatusEnum.unlabel) in states:
            mark_job_status = int(StatusEnum.labeling)
        elif int(StatusEnum.labeled) in states:
            mark_job_status = int(StatusEnum.reviewing)
        else:
            mark_job_status = int(StatusEnum.approved)
        return mark_job_status
