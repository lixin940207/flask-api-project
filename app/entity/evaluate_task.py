from app.common.extension import db
from app.model.base import BaseModel


class EvaluateTask(BaseModel):
    evaluate_task_id = db.Column(db.Integer(), primary_key=True)
    evaluate_task_name = db.Column(db.String(256), nullable=False)
    evaluate_task_desc = db.Column(db.Text(), default="")
    evaluate_task_status = db.Column(db.Integer(), db.ForeignKey("nlp_task.nlp_task_id"), nullable=False)
    evaluate_task_result = db.Column(db.JSON(), default={})
    train_task_id = db.Column(db.Integer(), db.ForeignKey("train_task.train_task_id"), nullable=False)
