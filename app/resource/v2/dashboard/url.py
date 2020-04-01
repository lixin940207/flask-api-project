# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from app.resource.v2.dashboard import api
from app.resource.v2.dashboard import view

api.add_resource(view.DashboardResource, "/")
api.add_resource(view.DemoResource, "/demo")
