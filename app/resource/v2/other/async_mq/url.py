# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-12:32 下午
from .. import api
from . import view

api.add_resource(view.AsyncMQResource, '/async')
