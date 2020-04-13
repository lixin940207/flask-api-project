# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-12:41 下午
from .. import api
from . import view

api.add_resource(view.MachineTaskListResource, '/machine')
api.add_resource(view.MachineTaskItemResource, '/machine/<int:task_id>')
