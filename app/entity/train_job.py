from app.common.extension import db
from app.entity.base import BaseEntity


class TrainJob(BaseEntity):
    train_job_id = db.Column(db.Integer(), primary_key=True)
    train_job_name = db.Column(db.String(256), nullable=False)
    train_job_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), nullable=False)
    train_job_desc = db.Column(db.Text(), default="")
    doc_type_id = db.Column(db.Integer(), db.ForeignKey("doc_type.doc_type_id"), nullable=False)
    preprocess = db.Column(db.JSON(), default={"split_by_sentence": True})  # 抽取：短文本
