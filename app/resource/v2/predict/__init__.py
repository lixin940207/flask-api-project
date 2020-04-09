# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:22 下午
from flask_restful import Api
from .. import blueprint

api = Api(blueprint, prefix='/extract', decorators=[])
