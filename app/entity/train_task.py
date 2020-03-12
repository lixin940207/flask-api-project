from app.common.extension import db
from app.entity.base import BaseEntity


class TrainTask(BaseEntity):
    train_model_id = db.Column(db.Integer(), primary_key=True)
    train_model_name = db.Column(db.String(256), nullable=False)
    train_model_desc = db.Column(db.Text(), default="")
    train_config = db.Column(db.JSON(), default={})
    train_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    model_version = db.Column(db.String(256), default="")
    train_job_id = db.Column(db.Integer(), db.ForeignKey("train_job.train_job_id"), nullable=False)
