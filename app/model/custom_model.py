from app.common.extension import db
from app.model.base import BaseModel


class CustomModel(BaseModel):
    custom_model_id = db.Column(db.Integer(), primary_key=True)
    custom_model_alias = db.Column(db.String(100), nullable=False)
    custom_model_name = db.Column(db.String(100), nullable=False)
    custom_model_desc = db.Column(db.String(256), default="")
    custom_model_ip = db.Column(db.String(256), nullable=False)
    custom_model_predict_port = db.Column(db.Integer(), nullable=False)
    custom_model_evaluate_port = db.Column(db.Integer(), nullable=False)
    custom_model_config = db.Column(db.JSON(), default={})
    custom_model_status = db.Column(db.Boolean(), default=False)
    nlp_task_id = db.Column(db.Integer(), db.ForeignKey("nlp_task.nlp_task_id"), nullable=False)

