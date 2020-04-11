from app.common.common import StatusEnum
from app.common.extension import db
from app.entity.base import BaseEntity


class UserTask(BaseEntity):
    user_task_id = db.Column(db.Integer(), primary_key=True)
    mark_task_id = db.Column(db.Integer(), db.ForeignKey('mark_task.mark_task_id'), nullable=False)
    annotator_id = db.Column(db.Integer(), nullable=False)
    user_task_result = db.Column(db.JSON(), default={})
    user_task_status = db.Column(db.Integer(), db.ForeignKey("status.status_id"), default=int(StatusEnum.processing))
