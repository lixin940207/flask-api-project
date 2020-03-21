# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask import g
from flask_restful import Resource
from app.model.doc_type_model import DocTypeModel
from app.common.extension import session
from app.entity.doc_type import DocType
from app.common.filters import QueryByRoleMixin
from app.service.dashboard_service import DashboardService
from app.common.seeds import NlpTaskEnum


class DemoResource(Resource):
    def get(self):

        pass


class DashboardResource(Resource, QueryByRoleMixin):
    def get(self):
        """
        获取分类、抽取、分词和实体关系的项目数量、标注任务数、模型数、已标注任务数、已审核任务数
        :return:
        """
        g.user_roles = ["管理员"]
        if self.get_current_role() in ['管理员', '超级管理员']:
            """
            管理员和超级管理员可以看到模型、标注信息
            """
            return DashboardService().get_dashboard_stats_manager()
        else:
            """
            非管理员角色不能看到模型信息，只能看到标注相关信息
            """
