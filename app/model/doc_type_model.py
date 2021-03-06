# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
from abc import ABC
from sqlalchemy import or_

from typing import List, Set

from app.entity import MarkJob, TrainJob, TrainTask, DocTerm
from app.model.base import BaseModel
from app.entity.doc_type import DocType
from app.common.extension import session
from app.common.common import RoleEnum, StatusEnum
from sqlalchemy import func
from app.common.filters import CurrentUser


class DocTypeModel(BaseModel, ABC):
    def get_all(self) -> List[DocType]:
        return session.query(DocType).filter(~DocType.is_deleted).all()

    def get_by_id(self, _id) -> DocType:
        return session.query(DocType).filter(DocType.doc_type_id == _id, ~DocType.is_deleted).one()

    def get_by_ids(self, ids) -> List[DocType]:
        return session.query(DocType).filter(DocType.doc_type_id.in_(ids), ~DocType.is_deleted).all()

    def get_by_id_by_user_group(self, _id, group_id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, DocType.group_id == group_id,
                                             ~DocType.is_deleted).one()

    def get_online_ids_by_ids(self, doc_type_ids) -> Set[int]:
        """获取拥有上线模型的doctype ids"""
        online_doc_types = session.query(DocType.doc_type_id).join(
            TrainJob, DocType.doc_type_id == TrainJob.doc_type_id
        ).join(
            TrainTask, TrainTask.train_job_id == TrainJob.train_job_id
        ).filter(
            TrainTask.train_status == int(StatusEnum.online),
            TrainJob.doc_type_id.in_(doc_type_ids),
            ~TrainJob.is_deleted,
            ~TrainTask.is_deleted
        ).all()
        online_doc_type_ids = set(item.doc_type_id for item in online_doc_types)
        return online_doc_type_ids

    @staticmethod
    def if_exists_by_name(doc_type_name):
        item = session.query(DocType).filter(DocType.doc_type_name == doc_type_name, DocType.status).first()
        return item

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0,
                      **kwargs) -> [DocType]:
        # Define allowed filter keys
        accept_keys = ["user_groups", "doc_type_name", "nlp_task_id", "doc_type_id", "group_id"]
        # Compose query
        q = session.query(DocType).filter(~DocType.is_deleted)
        # Filter conditions
        for key, val in kwargs.items():
            if key == "user_groups":
                q = q.filter(DocType.group_id.in_(val))
            elif key in accept_keys:
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

    def bulk_create(self, entity_list) -> List[DocType]:
        entity_list = [DocType(**entity) for entity in entity_list]
        session.bulk_save_objects(entity_list, return_defaults=True)
        session.flush()
        return entity_list

    def delete(self, _id) -> None:
        session.query(DocType).filter(DocType.doc_type_id == _id).update({DocType.is_deleted: True})
        session.flush()

    def bulk_delete(self, _id_list) -> None:
        session.query(DocType).filter(DocType.doc_type_id.in_(_id_list)).update({DocType.is_deleted: True})
        session.flush()

    def update(self, doc_type_id, **kwargs) -> DocType:
        accept_keys = ["doc_type_name", "doc_type_desc", "is_favorite", "group_id"]
        _doc_type = session.query(DocType).filter(DocType.doc_type_id == doc_type_id).one()
        for key, val in kwargs.items():
            if key in accept_keys:
                setattr(_doc_type, key, val)
        session.commit()

        return _doc_type

    def bulk_update(self, entity_list) -> None:
        session.bulk_update_mappings(DocType, entity_list)

    @staticmethod
    def count_doc_type_by_nlp_task(current_user: CurrentUser) -> [(int, int)]:
        q = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)) \
            .filter(~DocType.is_deleted)
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            # Reviewer and annotator joins mark_job to filter visible doc types
            q = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)) \
                .join(MarkJob, MarkJob.doc_type_id == DocType.doc_type_id) \
                .filter(~DocType.is_deleted, ~MarkJob.is_deleted,
                        or_(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)),
                            func.json_contains(MarkJob.annotator_ids, str(current_user.user_id))))
        count = q.group_by(DocType.nlp_task_id).all()
        return count

    def get_by_mark_job_id(self, mark_job_id):
        doc_type = session.query(DocType).join(
            MarkJob, DocType.doc_type_id == MarkJob.doc_type_id
        ).filter(
            MarkJob.mark_job_id == mark_job_id
        ).first()
        return doc_type

    @staticmethod
    def get_by_mark_job_ids(mark_job_ids, nlp_task_id, current_user: CurrentUser, limit=10, offset=0) -> (int, List):
        q = session.query(DocType)\
                .outerjoin(MarkJob, MarkJob.doc_type_id == DocType.doc_type_id)\
                .filter(DocType.nlp_task_id == nlp_task_id,
                        ~DocType.is_deleted,
                        or_(~MarkJob.is_deleted, MarkJob.is_deleted.is_(None)))
        # 权限filter
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            q = q.filter(or_(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)),
                             func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id))))
        if mark_job_ids:
            q = q.filter(MarkJob.mark_job_id.in_(mark_job_ids))
        count = q.count()
        items = q.offset(offset).limit(limit).all()
        return count, items

    @staticmethod
    def get_by_nlp_task_id_by_user(nlp_task_id, current_user: CurrentUser) -> [DocType]:
        q = session.query(DocType, func.group_concat(DocTerm.doc_term_id.distinct()))\
            .outerjoin(DocTerm, DocTerm.doc_type_id == DocType.doc_type_id)\
            .filter(DocType.nlp_task_id == nlp_task_id,
                    ~DocType.is_deleted,
                    or_(~DocTerm.is_deleted, DocTerm.is_deleted.is_(None)))
        # 权限filter
        if current_user.user_role in [RoleEnum.manager.value, RoleEnum.guest.value]:
            q = q.filter(DocType.group_id.in_(current_user.user_groups))
        elif current_user.user_role in [RoleEnum.reviewer.value, RoleEnum.annotator.value]:
            q = q.outerjoin(MarkJob, MarkJob.doc_type_id == DocType.doc_type_id)\
                    .filter(~MarkJob.is_deleted,
                            or_(func.json_contains(MarkJob.annotator_ids, str(current_user.user_id)),
                                func.json_contains(MarkJob.reviewer_ids, str(current_user.user_id))))
        q = q.group_by(DocTerm.doc_type_id, DocType)
        count = q.count()
        q = q.order_by(DocType.is_favorite.desc(), DocType.created_time.desc())
        return count, q.all()
