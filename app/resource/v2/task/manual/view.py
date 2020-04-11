# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: view.py 
@Time: 2020/04/11 13:54
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from flask_restful import Resource
from app.service.manual_task_service import ManualTaskService


class ManualTaskItemResource(Resource):
    def delete(self, task_id):
        ManualTaskService().detele_task(task_id)
        return {
                   "message": "删除成功",
               }, 204
