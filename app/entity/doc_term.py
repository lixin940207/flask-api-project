from app.common.extension import db
from app.entity.base import BaseEntity


class DocTerm(BaseEntity):
    doc_term_id = db.Column(db.Integer(), primary_key=True)
    doc_term_name = db.Column(db.String(256), nullable=False)
    doc_term_alias = db.Column(db.String(20), default="")
    doc_term_shortcut = db.Column(db.String(20), default="")
    doc_term_color = db.Column(db.String(256), default="")
    doc_term_desc = db.Column(db.Text(), default="")
    doc_term_index = db.Column(db.Integer(), default=1)
    doc_term_data_type = db.Column(db.String(256), default="")  # 字符、数字、布尔
    doc_type_id = db.Column(db.Integer(), db.ForeignKey('doc_type.doc_type_id'), nullable=False)

