# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_type_service.py 
@Time: 2020/03/26 16:56
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.common import Common
from app.model.doc_term_model import DocTermModel
from app.schema.doc_term_schema import DocTermSchema


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
        result = DocTermSchema(many=True).dump(item)
        return result
