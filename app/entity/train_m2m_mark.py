from app.common.extension import db
from app.entity.base import BaseEntity


class TrainM2mMark(BaseEntity):
    id = db.Column(db.Integer(), primary_key=True)
    train_job_id = db.Column(db.Integer(), db.ForeignKey('train_job.train_job_id'), nullable=False)
    mark_job_id = db.Column(db.Integer(), db.ForeignKey('mark_job.mark_job_id'), nullable=False)

# from sqlalchemy import Table, Integer, ForeignKey

# train_m2m_mark = Table(
#     'train_m2m_mark', db.metadata,
#     db.column('train_job_id', Integer(), ForeignKey('train_job.train_job_id')),
#     db.column('mark_job_id', Integer(), ForeignKey('mark_job.mark_job_id'))
# )


