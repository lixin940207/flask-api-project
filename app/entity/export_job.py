from app.common.extension import db
from app.entity.base import BaseEntity


class ExportJob(BaseEntity):
    export_job_id = db.Column(db.Integer(), primary_key=True)
    doc_type_id = db.Column(db.Integer(), db.ForeignKey('doc_type.doc_type_id'), nullable=False)
    export_file_path = db.Column(db.String(255), default="")
    export_job_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    export_mark_job_ids = db.Column(db.JSON(), default=[])
    export_predict_job_ids = db.Column(db.JSON(), default=[])

