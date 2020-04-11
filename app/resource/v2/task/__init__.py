from flask_restful import Api
from app.resource.v2 import blueprint
api = Api(blueprint, prefix='/task', decorators=[])

from app.resource.v2.task import manual, machine
