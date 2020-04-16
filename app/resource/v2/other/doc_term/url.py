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
api.add_resource(view.DocTermListResource, "/doc_type/<int:doc_type_id>/doc_term",
                 "/classify_doc_type/<int:doc_type_id>/classify_doc_term",
                 "/wordseg_doc_type/<int:doc_type_id>/wordseg_doc_term",
                 "/entity_doc_type/<int:doc_type_id>/entity_doc_term")
api.add_resource(view.ListWordsegDocTermResource, '/wordseg_doc_terms')
api.add_resource(view.EntityDocTermItemResource, '/entity_doc_type/<int:doc_type_id>/entity_doc_term/<int:doc_term_id>')

api.add_resource(view.WordsegDocLexiconListResource, '/wordseg_doc_type/<int:doc_type_id>/wordseg_doc_lexicon')
api.add_resource(view.WordsegDocLexiconItemResource,
                 '/wordseg_doc_type/<int:doc_type_id>/wordseg_doc_lexicon/<int:doc_lexicon_id>')

api.add_resource(view.ClassifyDocRuleListResource, '/classify_doc_type/<int:doc_type_id>/classify_doc_rule')
api.add_resource(view.ClassifyDocRuleItemResource,
                 '/classify_doc_type/<int:doc_type_id>/classify_doc_rule/<int:doc_rule_id>')
