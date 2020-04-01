from app.common.extension import db
from app.entity.base import BaseEntity


class MarkTask(BaseEntity):
    mark_task_id = db.Column(db.Integer(), primary_key=True)
    mark_job_id = db.Column(db.Integer(), db.ForeignKey('mark_job.mark_job_id'), nullable=False)
    doc_id = db.Column(db.Integer(), db.ForeignKey('doc.doc_id'), nullable=False)
    mark_task_result = db.Column(db.JSON(), default={})
    mark_task_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
