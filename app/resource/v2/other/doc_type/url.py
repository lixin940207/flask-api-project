# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: url.py.py 
@Time: 2020/03/26 16:23
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.resource.v2.other import api
from app.resource.v2.other.doc_type import view

api.add_resource(view.DocTypeListResource, '/doc_type', '/classify_doc_type', '/entity_doc_type', '/wordseg_doc_type')
