from app.common.extension import db
from app.entity.base import BaseEntity


class NlpTask(BaseEntity):
    nlp_task_id = db.Column(db.Integer(), primary_key=True)
    nlp_task_name = db.Column(db.String(50), nullable=False)
