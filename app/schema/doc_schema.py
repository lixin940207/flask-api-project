# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/25-3:50 下午
from flask_marshmallow import Schema


class DocSchema(Schema):  # type: ignore
    class Meta:
        fields = (
            'doc_id',
            'doc_unique_name',
            'doc_raw_name',
        )