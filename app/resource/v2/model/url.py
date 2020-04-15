# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-5:08 下午
from . import api
from . import view

# model list resources
api.add_resource(view.ModelListResource, '', '/entity_model', '/wordseg_model')
api.add_resource(view.ClassifyModelListResource, '/classify_model')

# single model resource
api.add_resource(view.ModelItemResource, '/<int:model_id>', '/classify_model/<int:model_id>', '/entity_model/<int:model_id>', '/wordseg_model/<int:model_id>')


# 首页的 doc_type_info resources
api.add_resource(view.DocTypeInfoListResource, '/doc_type_info', '/classify_doc_type_info', '/entity_doc_type_info', '/wordseg_doc_type_info')

# 上线模型信息的resources
api.add_resource(view.DocTypeLatestInfoResource, '/doc_type_latest_info', '/classify_doc_type_latest_info', '/entity_doc_type_latest_info', '/wordseg_doc_type_latest_info')
