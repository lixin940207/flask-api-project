# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask_restful import Api
from .. import blueprint

api = Api(blueprint, prefix='/model', decorators=[])

from . import view, url
from app.resource.v2.model import train, evaluate, custom
