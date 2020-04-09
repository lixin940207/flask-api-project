from .. import api
from . import view

api.add_resource(view.DocListResource, '/doc')
api.add_resource(view.DocItemResource, '/doc/<int:doc_id>')
