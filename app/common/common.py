# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
import os
import json
import datetime
from flask_restful import request
from enum import Enum


class NlpTaskEnum(int, Enum):
    extract = 1,
    classify = 2,
    wordseg = 3,
    relation = 4


class StatusEnum(int, Enum):
    init = 1,           # 标注任务、模型训练 - 初始化
    queueing = 2,       # 预处理、模型训练、预测 - 排队中
    processing = 3,     # 预处理处理中、自定义模型导出中
    unlabel = 4,        # 标注文件 - 待标注
    labeling = 5,       # 标注文件 - 标注中（保存但未提交）
    labeled = 6,        # 标注文件 - 已标注
    reviewing = 7,      # 标注文件、标注任务 - 审核中
    approved = 8,       # 标注文件、标注任务 - 审核通过
    training = 9,       # 模型 - 训练中
    evaluating = 10,    # 模型 - 评估中
    fail = 11,          # 预处理、模型训练、模型评估、模型预测 - 失败
    success = 12,       # 模型、评估、预测 - 完成
    online = 13,        # 模型 - 模型上线
    deleted = 14,       # 模型 - 已删除，目前没用，预留
    unavailable = 15,   # 自定义容器 - 服务不可用
    available = 16,     # 自定义容器 - 服务可用


class RoleEnum(str, Enum):
    admin = "超级管理员",
    manager = "管理员",
    reviewer = "审核员",
    annotator = "标注员",
    guest = "游客"


class Common:
    @staticmethod
    def make_dirs(path: str):
        path = path.strip()
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def get_csv(path: str):
        with open(os.path.join(os.getcwd(), path)) as f:
            data = f.read()
            # TODO process csv
        return data

    @staticmethod
    def get_json(path: str):
        with open(os.path.join(os.getcwd(), path)) as f:
            data = json.loads(f.read())
        return data

    @staticmethod
    def format_datetime(_datetime: datetime.datetime, format_string: str = '%Y%m%d%H%M%S'):
        return _datetime.strftime(format_string)

    @staticmethod
    def get_nlp_task_id_by_route(args=None):
        nlp_task_url = request.url.split('/')[-1]
        if 'classify' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.classify)
        elif 'entity' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.relation)
        elif 'wordseg' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.wordseg)
        else:
            nlp_task_id = int(NlpTaskEnum.extract)
        if args:
            args.update({
                'nlp_task_id': nlp_task_id
            })
        return nlp_task_id
