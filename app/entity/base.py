import typing
from flask import g
import datetime
from app.common.extension import db
from enum import Enum


def get_attr_from_g(name: str, default=None, raise_exception=True) -> typing.Any:
    def getter():
        if not hasattr(g, name):
            if raise_exception:
                raise AttributeError(f'flask g has not attribute {name}')
            return default
        return getattr(g, name)

    return getter


class BaseEntity(db.Model):
    __abstract__ = True

    app_id = db.Column(db.Integer(), default=get_attr_from_g('app_id'))
    created_by = db.Column(db.Integer(), default=get_attr_from_g('user_id'))
    created_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    updated_by = db.Column(db.Integer(), onupdate=get_attr_from_g('user_id'))
    updated_time = db.Column(db.DateTime(), onupdate=datetime.datetime.now())
    deleted_by = db.Column(db.Integer())
    deleted_time = db.Column(db.DateTime(), onupdate=datetime.datetime.now())
    is_deleted = db.Column(db.Boolean(), default=False)


class FileTypeEnum(str, Enum):
    # 电子文档
    e_doc = 'e_doc'
    # 纯文本
    text = 'text'
    # OCR
    ocr = 'ocr'


class AssignModeEnum(str, Enum):
    # 均分标注
    average = 'average'
    # 共同标注
    together = 'together'
