# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask_restful import Api
from app.resource.v2 import blueprint
api = Api(blueprint, prefix='', decorators=[])

from app.resource.v2.other import doc_type, doc_term, async_mq
