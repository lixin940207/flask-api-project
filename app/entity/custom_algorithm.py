from app.common.extension import db
from app.entity.base import BaseEntity


class CustomAlgorithm(BaseEntity):
    custom_algorithm_id = db.Column(db.Integer(), primary_key=True)
    custom_algorithm_alias = db.Column(db.String(100), nullable=False)
    custom_algorithm_name = db.Column(db.String(100), nullable=False)
    custom_algorithm_desc = db.Column(db.String(256), default="")
    custom_algorithm_ip = db.Column(db.String(256), nullable=False)
    custom_algorithm_predict_port = db.Column(db.Integer(), nullable=False)
    custom_algorithm_evaluate_port = db.Column(db.Integer(), nullable=False)
    custom_algorithm_config = db.Column(db.JSON(), default={})
    custom_algorithm_status = db.Column(db.Boolean(), default=False)
    nlp_task_id = db.Column(db.Integer(), db.ForeignKey("nlp_task.nlp_task_id"), nullable=False)

