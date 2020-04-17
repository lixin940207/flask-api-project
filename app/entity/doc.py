from app.common.common import StatusEnum
from app.common.extension import db
from app.entity.base import BaseEntity


class Doc(BaseEntity):
    doc_id = db.Column(db.Integer(), primary_key=True)
    doc_unique_name = db.Column(db.String(64), nullable=False)
    doc_raw_name = db.Column(db.String(255), nullable=False)
    doc_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), default=StatusEnum.processing.value, nullable=False)
