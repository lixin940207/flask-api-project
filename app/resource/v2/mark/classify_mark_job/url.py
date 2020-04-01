# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
from app.resource.v2.mark import api
from . import view

api.add_resource(view.ClassifyMarkJobListResource, '/classify_mark_job')
