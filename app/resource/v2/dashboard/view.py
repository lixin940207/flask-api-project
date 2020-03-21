# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask import g
from flask_restful import Resource
from app.model.doc_type_model import DocTypeModel
from app.common.extension import session
from app.entity.doc_type import DocType


class DemoResource(Resource):
    def get(self):
        DocTypeModel().create(DocType(doc_type_name="测试分类项目", nlp_task_id=1))
        doc_type_list = [DocType(doc_type_name="测试分类项目{}".format(i), nlp_task_id=1) for i in range(5)]
        DocTypeModel().bulk_create(doc_type_list)
        DocTypeModel().get_all()
        DocTypeModel().delete(7)

        session.commit()