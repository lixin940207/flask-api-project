from app.common.extension import db
from app.entity.base import BaseEntity


class Status(BaseEntity):
    status_id = db.Column(db.Integer(), primary_key=True)
    status_name = db.Column(db.String(50), nullable=False)
