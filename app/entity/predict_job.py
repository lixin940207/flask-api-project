from app.common.extension import db
from app.entity.base import BaseEntity, FileTypeEnum


class PredictJob(BaseEntity):
    predict_job_id = db.Column(db.Integer(), primary_key=True)
    doc_type_id = db.Column(db.Integer(), db.ForeignKey("doc_type.doc_type_id"), nullable=False)
    predict_job_name = db.Column(db.String(256), default="")
    predict_job_type = db.Column(db.Enum(FileTypeEnum))
    predict_job_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    predict_job_desc = db.Column(db.Text(), default="")
