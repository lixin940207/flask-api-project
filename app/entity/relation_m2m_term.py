from app.common.extension import db
from app.model.base import BaseModel


class RelationM2mTerm(BaseModel):
    doc_relation_id = db.Column(db.Integer(), db.ForeignKey('doc_relation.doc_relation_id'), nullable=False)
    doc_term_id = db.Column(db.Integer(), db.ForeignKey('doc_term.doc_term_id'), nullable=False)
