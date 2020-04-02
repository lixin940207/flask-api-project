# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/30-5:39 下午
from app.common.extension import db
from app.entity.base import BaseEntity


class EvaluateM2mMark(BaseEntity):
    id = db.Column(db.Integer(), primary_key=True)
    evaluate_task_id = db.Column(db.Integer(), db.ForeignKey('evaluate_task.evaluate_task_id'), nullable=False)
    mark_job_id = db.Column(db.Integer(), db.ForeignKey('mark_job.mark_job_id'), nullable=False)