# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-2:56 下午
from .. import api
from . import view, backend

api.add_resource(view.CustomListResource, '/custom')
api.add_resource(view.CustomItemResource, '/custom/<int:custom_id>')

api.add_resource(view.CheckCustomIdNameResource, '/custom/check_id_name')
api.add_resource(view.CustomModelExportResource, '/custom/export/<int:custom_id>')

api.add_resource(backend.UpdateCustomModelResource, '/custom/update_export_state')