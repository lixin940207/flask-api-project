# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/13-10:40 上午
from .. import api
from . import view, backend

api.add_resource(view.WordsegMarkJobListResource, '/wordseg_mark_job')
api.add_resource(view.WordsegMarkJobItemResource, '/wordseg_mark_job/<int:job_id>')
api.add_resource(view.WordsegMarkJobMultiDelete, '/wordseg_jobs_multi_delete')
api.add_resource(backend.GetWordsegMarkJobDataResource, '/get_wordseg_mark_job_data')

api.add_resource(view.WordsegMarkJobImportResource, '/labeled_wordseg')
api.add_resource(view.WordsegMarkJobExportResource, '/export_wordseg_mark_job/<int:job_id>')

api.add_resource(view.WordsegMarkJobRePreLabelResource, '/wordseg_reprelabel')

# backend
api.add_resource(backend.GetWordsegMarkJobDataResource, '/get_wordseg_mark_job_data')
