from flask_restful import Api
from .. import blueprint

api = Api(blueprint, prefix='/export_history', decorators=[])

from app.resource.v2.export import url, view
