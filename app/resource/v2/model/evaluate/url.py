# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/2-6:50 下午
from .. import api
from . import view, backend

api.add_resource(view.ModelEvaluateListResource, '/<int:model_id>/evaluate')
api.add_resource(view.ModelEvaluateItemResource, '/<int:model_id>/evaluate/<int:model_evaluate_id>')

# backend
api.add_resource(backend.UpdateModelEvaluateResource, '/update_model_evaluate')
