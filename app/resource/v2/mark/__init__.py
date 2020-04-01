# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask_restful import Api
from .. import blueprint

api = Api(blueprint, prefix='/mark', decorators=[])

from app.resource.v2.mark import classify_mark_job
