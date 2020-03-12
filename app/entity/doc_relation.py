from app.common.extension import db
from app.model.base import BaseModel


class DocRelation(BaseModel):
    doc_relation_id = db.Column(db.Integer(), primary_key=True)
    doc_relation_name = db.Column(db.String(256), nullable=False)
    doc_relation_color = db.Column(db.String(256), default="")
    doc_relation_desc = db.Column(db.Text(), default="")
    doc_type_id = db.Column(db.Integer(), db.ForeignKey('doc_type.doc_type_id'), nullable=False)

