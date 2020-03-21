# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask_restful import Api
from app.resource.v2 import blueprint
api = Api(blueprint, prefix='/dashboard', decorators=[])

from . import view, url