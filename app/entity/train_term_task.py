from app.common.extension import db
from app.entity.base import BaseEntity


class TrainTermTask(BaseEntity):
    train_term_task_id = db.Column(db.Integer(), primary_key=True)
    train_term_result = db.Column(db.JSON(), default={})
    train_term_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    train_task_id = db.Column(db.Integer(), db.ForeignKey("train_task.train_task_id"), nullable=False)
    doc_term_id = db.Column(db.Integer(), db.ForeignKey("doc_term.doc_term_id"))
