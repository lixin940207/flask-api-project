from app.common.extension import db
from app.entity.base import BaseEntity


class Doc(BaseEntity):
    doc_id = db.Column(db.Integer(), primary_key=True)
    doc_unique_name = db.Column(db.String(64), nullable=False)
    doc_raw_name = db.Column(db.String(255), nullable=False)
