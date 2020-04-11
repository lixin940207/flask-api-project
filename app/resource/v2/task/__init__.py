# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/11-1:39 下午
from flask_restful import Api
from .. import blueprint

api = Api(blueprint, prefix='/task', decorators=[])

from . import machine, manual