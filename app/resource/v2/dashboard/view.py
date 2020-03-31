# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/18
from flask import g
from flask_restful import Resource
from app.model.doc_type_model import DocTypeModel
from app.common.extension import session
from app.entity.doc_type import DocType
from app.common.filters import CurrentUserMixin
from app.service.dashboard_service import DashboardService
from app.common.common import NlpTaskEnum, RoleEnum
from flask import jsonify


class DemoResource(Resource):
    def get(self):
        return jsonify(DocTypeModel().get_all())


class DashboardResource(Resource):
    def get(self):
        """
        获取分类、抽取、分词和实体关系的项目数量、标注任务数、模型数、已标注任务数、已审核任务数
        :return:
        """
        result_skeleton = [
            {"type": "分类项目", "nlp_task_id": int(NlpTaskEnum.classify)},
            {"type": "抽取项目", "nlp_task_id": int(NlpTaskEnum.extract)},
            {"type": "实体关系", "nlp_task_id": int(NlpTaskEnum.relation)},
            {"type": "分词项目", "nlp_task_id": int(NlpTaskEnum.wordseg)},
        ]
        if self.get_current_role() in [str(RoleEnum.manager), str(RoleEnum.admin), str(RoleEnum.guest)]:
            """
            管理员和超级管理员可以看到模型、标注信息
            """
            result_skeleton = DashboardService().get_dashboard_stats_manager(result_skeleton, g.user_id)
        else:
            """
            非管理员角色不能看到模型信息，只能看到标注相关信息
            """
            result_skeleton = DashboardService().dashboard_stats_reviewer_annotator(result_skeleton, g.user_id)

        return result_skeleton
