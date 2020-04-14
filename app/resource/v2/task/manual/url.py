# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: url.py 
@Time: 2020/04/11 13:54
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from .. import api
from . import view

api.add_resource(view.ManualTaskItemResource, '/manual/<int:task_id>')
api.add_resource(view.RejectManualTaskResource, '/reject_manual_task/<int:task_id>')
api.add_resource(view.TaskListResource, '/assess_task', '/label_task')
api.add_resource(view.TaskItemResource, '/label_task/<int:task_id>', '/assess_task/<int:task_id>')
api.add_resource(view.TaskItemNextResource, '/label_task/next/<int:task_id>', '/assess_task/next/<int:task_id>')
api.add_resource(view.AssessTaskItemPdfPrintResource, '/assess_task/print/<int:task_id>')
