# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/13-10:40 上午
from .. import api
from . import view

api.add_resource(view.WordsegMarkJobExportResource,'/export_wordseg_mark_job/<int:job_id>')
