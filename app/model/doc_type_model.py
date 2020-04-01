# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
from abc import ABC
from sqlalchemy import func, or_
from app.entity import MarkJob

import typing

from app.entity import MarkJob
from app.model.base import BaseModel
from app.entity.doc_type import DocType
from app.common.extension import session
from app.common.common import RoleEnum
from sqlalchemy import func
from app.common.filters import CurrentUser


class DocTypeModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocType).filter(~DocType.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, ~DocType.is_deleted).one()

    def get_by_id_by_user_group(self, _id, group_id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, DocType.group_id == group_id,
                                             ~DocType.is_deleted).one()

    def get_by_filter(self, current_user: CurrentUser, order_by="created_time", order_by_desc=True, limit=10, offset=0,
                      **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_type_name", "nlp_task_id", "doc_type_id", "group_id"]
        # Compose query
        q = session.query(DocType).filter(DocType.group_id.in_(current_user.user_groups), ~DocType.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(DocType, key) == val)
        # Order by key
        if order_by_desc:
            q = q.order_by(getattr(DocType, order_by).desc())
        else:
            q = q.order_by(getattr(DocType, order_by))
        q = q.offset(offset).limit(limit)
        return q.all()

    def create(self, **kwargs) -> DocType:
        entity = DocType(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id):
        session.query(DocType).filter(DocType.doc_type_id == _id).update({DocType.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list):
        session.query(DocType).filter(DocType.doc_type_id.in_(_id_list)).update({DocType.is_deleted: True})
        session.flush()

    def update(self, entity):
        # session.bulk_update_mappings
        pass

    def bulk_update(self, entity_list) -> None:
        session.bulk_update_mappings(DocType, entity_list)

    @staticmethod
    def count_doc_type_by_nlp_task(current_user: CurrentUser):
        q = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)) \
            .filter(~DocType.is_deleted)
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            # Reviewer and annotator joins mark_job to filter visible doc types
            q = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)) \
                .join(MarkJob, MarkJob.doc_type_id == DocType.doc_type_id) \
                .filter(~DocType.is_deleted, ~MarkJob.is_deleted,
                        or_(func.json_contains(MarkJob.annotator_ids, current_user.user_id),
                            func.json_contains(MarkJob.annotator_ids, current_user.user_id)))
        count = q.group_by(DocType.nlp_task_id).all()
        return count

    @staticmethod
    def get_by_mark_job_ids(mark_job_ids, nlp_task_id, current_user: CurrentUser, limit=10, offset=0) -> (
    typing.List, int):
        q = session.query(DocType).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted)
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            q = q.fitler(func.json_contains(MarkJob.annotator_ids, current_user.user_id))
        if mark_job_ids:
            q = q.outerjoin(MarkJob, MarkJob.doc_type_id == DocType.doc_type_id) \
                .filter(MarkJob.mark_job_id.in_(mark_job_ids))
        count = q.count()
        items = q.offset(offset).limit(limit).all()
        return items, count

    @staticmethod
    def get_by_nlp_task_id_by_user(nlp_task_id, current_user: CurrentUser):
        q = session.query(DocType).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted)
        if current_user.user_role == "管理员":
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role == "审核员":
            q = q.join(MarkJob, DocType.doc_type_id == MarkJob.doc_type_id) \
                .filter(~MarkJob.is_deleted,
                        func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id)))
        elif current_user.user_role == "标注员":
            q = q.join(MarkJob, DocType.doc_type_id == MarkJob.doc_type_id) \
                .filter(~MarkJob.is_deleted,
                        func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)))
        q = q.order_by(DocType.created_time.desc())
        return q.all()
