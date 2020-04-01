# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/24-3:29 下午
from .. import api
from . import view

api.add_resource(view.ModelTrainListResource, '/<int:model_id>/train')
api.add_resource(view.ModelTrainItemResource, '/<int:model_id>/train/<int:model_train_id>')
api.add_resource(view.TrainTermListResource, '/<int:model_id>/train/<int:model_train_id>/term')
api.add_resource(view.TrainTermItemResource, '/<int:model_id>/train/<int:model_train_id>/term/<int:train_term_id>')
