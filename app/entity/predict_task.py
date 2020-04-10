from app.common.extension import db
from app.entity.base import BaseEntity


class PredictTask(BaseEntity):
    predict_task_id = db.Column(db.Integer(), primary_key=True)
    doc_id = db.Column(db.Integer(), db.ForeignKey("doc.doc_id"), nullable=False)
    predict_task_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    predict_task_result = db.Column(db.JSON(), default={})
    predict_job_id = db.Column(db.Integer(), db.ForeignKey("predict_job.predict_job_id"), nullable=False)
