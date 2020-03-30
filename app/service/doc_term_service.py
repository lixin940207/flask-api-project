# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_type_service.py 
@Time: 2020/03/26 16:56
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.model.doc_term_model import DocTermModel


class DocTermService:
    @staticmethod
    def get_doc_term_list(user_id, user_role, args):
        exclude_terms_ids = args.get('exclude_terms_ids', [])
        offset = args.get('offset', 0)
        limit = args.get('limit', 10)
        result, count = DocTermModel().get_by_exclude_terms(exclude_terms_ids=exclude_terms_ids, offset=offset,
                                                            limit=limit)
        return result, count
