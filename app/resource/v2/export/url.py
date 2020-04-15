from . import api
from . import view

api.add_resource(view.ExportHistoryResource, "")
api.add_resource(view.ExportHistoryItemResource, "/<int:export_id>")
