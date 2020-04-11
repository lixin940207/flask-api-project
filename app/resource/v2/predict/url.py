# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/9-2:21 下午
from . import api
from . import view

api.add_resource(view.ExtractJobListResource, '/extract_job', '/classify_extract_job', '/entity_extract_job', '/wordseg_extract_job')
api.add_resource(view.ExtractJobItemResource, '/extract_job/<int:job_id>', '/classify_extract_job/<int:job_id>', '/entity_extract_job/<int:job_id>', '/wordseg_extract_job/<int:job_id>')
api.add_resource(view.ExtractJobExportResource, '/export_extract_job/<int:job_id>', '/export_classify_extract_job/<int:job_id>', '/export_wordseg_extract_job/<int:job_id>')