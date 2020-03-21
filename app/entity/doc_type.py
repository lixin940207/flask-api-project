from app.common.extension import db
from app.entity.base import BaseEntity


class DocType(BaseEntity):
    doc_type_id = db.Column(db.Integer(), primary_key=True)
    doc_type_name = db.Column(db.String(255), nullable=False)
    doc_type_desc = db.Column(db.Text(), default="")
    is_favorite = db.Column(db.Boolean(), default=False)
    nlp_task_id = db.Column(db.Integer(), db.ForeignKey("nlp_task.nlp_task_id"), nullable=False)
