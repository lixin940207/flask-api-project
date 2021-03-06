# coding=utf-8
# @Author: Gu
# @Date: 2020/3/23
from app.resource.v2.mark import api
from . import view

api.add_resource(view.ClassifyMarkJobListResource, '/classify_mark_job')
api.add_resource(view.ClassifyMarkJobItemResource, '/classify_mark_job/<int:job_id>')

api.add_resource(view.ClassifyMarkJobImportResource, '/labeled_classify')
api.add_resource(view.ClassifyMarkJobMultiDelete, '/classify_jobs_multi_delete')

api.add_resource(view.ClassifyMarkJobExportResource, '/export_classify_mark_job/<int:job_id>')
api.add_resource(view.ClassifyMarkJobMultiExportResource, '/export_classify_mark_job')
api.add_resource(view.ClassifyMarkJobRePreLabelResource, '/classify_reprelabel')
