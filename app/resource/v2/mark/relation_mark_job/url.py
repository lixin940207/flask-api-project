from .. import api
from . import view, backend

api.add_resource(view.RelationMarkJobListResource, '/entity_mark_job')
api.add_resource(view.RelationMarkJobItemResource, '/entity_mark_job/<int:job_id>')
api.add_resource(view.RelationMarkJobMultiDelete, '/entity_jobs_multi_delete')

# backend
api.add_resource(backend.GetRelationMarkJobDataResource, '/get_entity_mark_job_data')
