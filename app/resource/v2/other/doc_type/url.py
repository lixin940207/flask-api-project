# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@Time: 2020/03/26 16:23
@Email: guochuanxiang@datagrand.com
"""
from app.resource.v2.other import api
from app.resource.v2.other.doc_type import view

api.add_resource(view.DocTypeListResource, '/doc_type', '/classify_doc_type', '/entity_doc_type', '/wordseg_doc_type')
api.add_resource(view.DocTypeItemResource, '/classify_doc_type/<int:doc_type_id>',
                 '/doc_type/<int:doc_type_id>', '/wordseg_doc_type/<int:doc_type_id>')
api.add_resource(view.RelationDocTypeItemResource, '/entity_doc_type/<int:doc_type_id>')
api.add_resource(view.EntityDocRelationListResource, '/entity_doc_type/<int:doc_type_id>/entity_doc_relation')

api.add_resource(view.TopDocTypeResource,
                 '/topping_doc_type/<int:doc_type_id>',
                 '/topping_classify_doc_type/<int:doc_type_id>',
                 '/topping_wordseg_doc_type/<int:doc_type_id>',
                 '/topping_entity_doc_type/<int:doc_type_id>')
api.add_resource(view.CancelTopDocTypeResource,
                 '/cancel_topping_doc_type/<int:doc_type_id>',
                 '/cancel_topping_classify_doc_type/<int:doc_type_id>',
                 '/cancel_topping_wordseg_doc_type/<int:doc_type_id>',
                 '/cancel_topping_entity_doc_type/<int:doc_type_id>')

# api.add_resource(view.CheckDocTypeItemResource, '/check_doc_type')
