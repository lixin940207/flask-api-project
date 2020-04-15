# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/15
import json
import typing
import uuid
from datetime import datetime

from app.common.extension import session
from app.config.config import get_config_from_app as _get
from app.common.filters import CurrentUser
from app.common.redis import r
from app.model import MarkJobModel, DocTermModel
from app.model.export_job_model import ExportJobModel
from app.model.relation_m2m_term_model import RelationM2mTermModel
from app.schema.export_job_schema import ExportJobSchema


class ExportService:
    @staticmethod
    def get_export_history(current_user: CurrentUser, args):
        items, count = ExportJobModel().get_export_history(current_user, args.get("offset"), args.get("limit"))
        return ExportJobSchema(many=True).dump(items), count

    @staticmethod
    def create_export_task(current_user: CurrentUser, mark_job_ids, mark_type, export_type):
        # raise no result found exception
        redis_message = {}
        doc_type_id = MarkJobModel().get_by_id(int(mark_job_ids.split(',')[0])).doc_type_id
        doc_terms = [str(row.doc_term_id) for row in DocTermModel().get_by_filter(doc_type_id=doc_type_id)]
        if mark_type == 'wordseg':
            doc_terms = ['10086']
        elif mark_type == 'relation':
            relation_2_entity_mapping = [{i[0]: [d for d in i[1].split(",")]} for i in RelationM2mTermModel.get_relation_term_mapping(doc_type_id)]
            redis_message.update({
                'relation_2_entity_mapping': relation_2_entity_mapping,
            })
        version = '{}{}_{}_{}'.format(datetime.now().strftime("%Y%m%d%H%M%S"), str(uuid.uuid4())[:4], doc_type_id,
                                      mark_job_ids)
        file_path = 'upload/export/{}.zip'.format(version)

        new_export_job = ExportJobModel().create({
            "file_path": file_path,
            "mark_type": mark_type,
            "doc_type_id": doc_type_id,
            "export_by": current_user.user_id,
            "export_state": "processing",
            "export_mark_job_ids": [int(i) for i in mark_job_ids.split(',')]
        })
        export_id = new_export_job.export_id

        session.commit()
        # 发送给offline nlp
        redis_message.update({
            'export_id': export_id,
            'export_type': export_type,
            'file_path': file_path,
            'version': version,
            'doc_type': doc_type_id,
            'fields': ','.join(doc_terms),
            'mark_job_ids': mark_job_ids,
            'task_type': mark_type,
        })
        r.lpush(_get('DATA_EXPORT_QUEUE_KEY'), json.dumps(redis_message))

    @staticmethod
    def delete_by_id(export_id):
        ExportJobModel().delete(export_id)
        session.commit()

    @staticmethod
    def update_status(export_id, status):
        ExportJobModel().update_status(export_id, status)
        session.commit()
