# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_type_service.py 
@Time: 2020/03/26 16:56
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.extension import session
from app.model import DocTermModel
from app.schema import DocTermSchema


class DocTermService:
    @staticmethod
    def get_doc_term_list(args):
        exclude_terms_ids = args.get('exclude_terms_ids', [])
        offset = args.get('offset', 0)
        limit = args.get('limit', 10)
        items, count = DocTermModel().get_by_exclude_terms(exclude_terms_ids=exclude_terms_ids, offset=offset,
                                                           limit=limit)
        result = DocTermSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def get_doc_term_by_doctype(doc_type_id, offset=0, limit=10, doc_term_ids=None):
        items, count = DocTermModel().get_doc_term_by_doctype(doc_type_id, offset, limit, doc_term_ids)
        result = DocTermSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def create_doc_term(args, doc_type_id):
        item = DocTermModel().create(**args, doc_type_id=doc_type_id)
        session.commit()
        result = DocTermSchema().dump(item)
        return result

    @staticmethod
    def check_term_in_relation(doc_term_id):
        return DocTermModel().check_term_in_relation(doc_term_id)

    @staticmethod
    def remove_doc_term(doc_term_id):
        DocTermModel().delete(doc_term_id)

    @staticmethod
    def update_doc_term(doc_term_id, args):
        item = DocTermModel().update(doc_term_id, **args)
        session.commit()
        result = DocTermSchema().dump(item)
        return result
