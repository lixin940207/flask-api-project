from app.common.extension import db
from app.model.base import BaseModel


class Status(BaseModel):
    status_id = db.Column(db.Integer(), primary_key=True)
    status_name = db.Column(db.String(50), nullable=False)
