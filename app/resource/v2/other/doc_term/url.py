# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: url.py.py 
@Time: 2020/03/26 16:23
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.resource.v2.other import api
from app.resource.v2.other.doc_term import view

api.add_resource(view.GetDocTermListResource, "/list_doc_terms", "/list_classify_doc_terms", "/list_entity_doc_terms")
