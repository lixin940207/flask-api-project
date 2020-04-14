from .. import api
from . import view, backend

api.add_resource(view.ExtractMarkJobListResource, '/mark_job')
api.add_resource(view.ExtractMarkJobItemResource, '/mark_job/<int:job_id>')
api.add_resource(view.ExtractMarkJobMultiDelete, '/jobs_multi_delete')
# 标注导入
api.add_resource(view.ExtractMarkJobImportResource, '/labeled_extract')
# 重新预标注
api.add_resource(view.ExtractMarkJobRePreLabelResource, '/extract_reprelabel')
# backend
api.add_resource(backend.GetExtractMarkJobDataResource, '/get_mark_job_data')
