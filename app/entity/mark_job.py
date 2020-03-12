from app.common.extension import db
from app.entity.base import BaseEntity, FileTypeEnum, AssignModeEnum


class MarkJob(BaseEntity):
    mark_job_id = db.Column(db.Integer(), primary_key=True)
    doc_type_id = db.Column(db.Integer(), db.ForeignKey("doc_type.doc_type_id"), nullable=False)
    mark_job_name = db.Column(db.String(255), nullable=False)
    mark_job_desc = db.Column(db.Text(), default="")
    mark_job_type = db.Column(db.Enum(FileTypeEnum), nullable=False)  # text, e_doc, ocr
    mark_job_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    assign_mode = db.Column(db.Enum(AssignModeEnum), nullable=False)  # average,
