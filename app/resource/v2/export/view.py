from typing import Tuple, Dict, Any
from flask_restful import Resource, abort

from app.common.filters import CurrentUserMixin
from app.common.patch import parse, fields
from app.service.export_service import ExportService

DB_TABLE_2_BUSINESS_MAPPING = {
    'mark': 'extract',
    'wordseg_mark': 'wordseg',
    'entity_mark': 'relation',
    'classify_mark': 'classify',
    'extract': 'extract',
    'wordseg': 'wordseg',
}


class ExportHistoryResource(Resource, CurrentUserMixin):
    @parse({
        "query": fields.String(missing=""),
        "offset": fields.Integer(missing=0),
        "limit": fields.Integer(missing=10),
        "model_type": fields.String(missing="",
                                    validate=lambda x: x in ('', 'extract', 'classify', 'relation', 'wordseg'))
    })
    def get(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        获取标注导出记录
        """
        result, count = ExportService().get_export_history(self.get_current_user(), args)
        return {
                   "message": "请求成功",
                   "result": result,
                   "count": count,
               }, 200

    @parse({
        "mark_type": fields.String(required=True, validate=lambda x: x in (
                DB_TABLE_2_BUSINESS_MAPPING)),
        "mark_job_ids": fields.String(required=True),
        "export_type": fields.String(required=True, validate=lambda x: x in ('BMES', 'BIO', 'label_analysis', 'all')),
    })
    def post(self: Resource, args: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        新建标注导出记录
        """
        mark_job_ids = args.get('mark_job_ids')
        mark_type = args.get('mark_type')
        if mark_type in DB_TABLE_2_BUSINESS_MAPPING:
            mark_type = DB_TABLE_2_BUSINESS_MAPPING[mark_type]
        else:
            abort(400, message='不支持的任务类型')
        export_type = args.get('export_type')
        ExportService().create_export_task(self.get_current_user(), mark_job_ids, mark_type, export_type)
        return {
                   "message": "创建成功",
               }, 201


class ExportHistoryItemResource(Resource):
    @parse({
        "export_state": fields.String(required=True,
                                      validate=lambda x: x in ('processing', 'failed', 'success'))
    })
    def put(self: Resource, args: Dict[str, Any], export_id: int) -> Tuple[Dict, int]:
        ExportService().update_status(export_id, args.get("export_state"))

        return {
                   "message": "状态更新成功",
               }, 200

    def delete(self: Resource, export_id: int) -> Tuple[Dict, int]:
        # Delete export_history record
        ExportService().delete_by_id(export_id)
        return {
                   "message": "删除成功",
               }, 200
