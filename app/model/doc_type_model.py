# coding=utf-8
# @Author: James Gu
# @Date: 2020/3/12
from abc import ABC
from sqlalchemy import func as sa_func
from app.entity import MarkJob
from app.model.base import BaseModel
from app.entity.doc_type import DocType
from app.common.extension import session
from sqlalchemy import func


class DocTypeModel(BaseModel, ABC):
    def get_all(self):
        return session.query(DocType).filter(~DocType.is_deleted).all()

    def get_by_id(self, _id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, ~DocType.is_deleted).one()

    def get_by_id_by_user_group(self, _id, group_id):
        return session.query(DocType).filter(DocType.doc_type_id == _id, DocType.group_id == group_id, ~DocType.is_deleted).one()

    def get_by_filter(self, order_by="created_time", order_by_desc=True, limit=10, offset=0, **kwargs):
        # Define allowed filter keys
        accept_keys = ["doc_type_name", "nlp_task_id", "doc_type_id", "group_id"]
        # Compose query
        q = session.query(DocType).filter(~DocType.is_deleted)
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

    def create(self, entity: DocType) -> DocType:
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

    def bulk_update(self, entity_list):
        session.bulk_update_mappings(DocType, entity_list)

    @staticmethod
    def count_doc_type_by_nlp_task_manager(user_id):
        count = session.query(DocType.nlp_task_id, func.count(DocType.doc_type_id)).filter(~DocType.is_deleted,
                                                                                           DocType.created_by == user_id) \
            .group_by(DocType.nlp_task_id).all()
        return count

    @staticmethod
    def get_by_nlp_task_id_by_user(nlp_task_id, user_role, user_id):
        q = session.query(DocType).filter(DocType.nlp_task_id == nlp_task_id, ~DocType.is_deleted)
        if user_role == "管理员":
            q = q.filter(DocType.created_by == user_id)
        elif user_role == "审核员":
            q = q.join(MarkJob, DocType.doc_type_id == MarkJob.doc_type_id)\
                .filter(~MarkJob.is_deleted,
                        sa_func.json_contains(MarkJob.reviewer_ids, str(user_id)))
        elif user_role == "标注员":
            q = q.join(MarkJob, DocType.doc_type_id == MarkJob.doc_type_id)\
                .filter(~MarkJob.is_deleted,
                        sa_func.json_contains(MarkJob.annotator_ids, str(user_id)))
        q = q.order_by(DocType.created_time.desc())
        return q.all()