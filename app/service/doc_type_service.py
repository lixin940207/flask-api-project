# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_type_service.py 
@Time: 2020/03/27 10:30
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.extension import session
from app.model import DocTypeModel
from app.model.doc_term_model import DocTermModel
from app.schema.doc_type_schema import DocTypeSchema


class DocTypeService:
    @staticmethod
    def get_doc_type(user_id, user_role, args):
        offset = args.get('offset', 0)
        limit = args.get('limit', 10)
        mark_job_ids = args.get('mark_job_ids', [])
        nlp_task_id = args.get('nlp_task_id')
        items, count = DocTypeModel().get_by_mark_job_ids(mark_job_ids=mark_job_ids, nlp_task_id=nlp_task_id, offset=offset, limit=limit)
        result = DocTypeSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def create_doc_type(user_id, user_role, args):
        doc_term_list = args.pop('doc_term_list')
        doc_type = DocTypeModel().create(**args)
        for item in doc_term_list:
            item.update({'doc_type_id': doc_type.doc_type_id})
        doc_type.doc_term_list = DocTermModel().bulk_create(doc_term_list)
        session.commit()
        result = DocTypeSchema().dumps(doc_type)
        return result
