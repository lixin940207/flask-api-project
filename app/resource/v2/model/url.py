# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-5:08 下午
from . import api
from . import view

# model list resources
api.add_resource(view.ModelListResource, '')
api.add_resource(view.ClassifyModelListResource, '/classify_model')
api.add_resource(view.RelationModelListResource, '/entity_model')
api.add_resource(view.WordsegModelListResource, '/wordseg_model')

#
api.add_resource(view.DocTypeInfoListResource, '/doc_type_info')


