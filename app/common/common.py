# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
import os
import json
import datetime
from flask_restful import request
from enum import Enum

from app.common.utils.name import get_ext


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
    def get_nlp_task_id_by_route():
        nlp_task_url = request.url
        if 'classify' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.classify)
        elif 'entity' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.relation)
        elif 'wordseg' in nlp_task_url:
            nlp_task_id = int(NlpTaskEnum.wordseg)
        else:
            nlp_task_id = int(NlpTaskEnum.extract)
        return nlp_task_id

    @staticmethod
    def get_wordseg_doc_terms():
        doc_terms = [
            dict(name='n', desc='名词', color='#d4380d'),
            dict(name='nr', desc='人名', color='#d4b106'),
            dict(name='ns', desc='地名', color='#096dd9'),
            dict(name='nt', desc='机构团体名', color='#389e0d'),
            dict(name='nz', desc='其他专名', color='#0d519e'),
            dict(name='t', desc='时间词', color='#c41d5c'),
            dict(name='s', desc='处所词', color='#cf1322'),
            dict(name='f', desc='方位词', color='#c41d7f'),
            dict(name='v', desc='动词', color='#08979c'),
            dict(name='a', desc='形容词', color='#1d39c4'),
            dict(name='b', desc='区别词', color='#d48806'),
            dict(name='z', desc='状态词', color='#b4ac2c'),
            dict(name='r', desc='代词', color='#d45d06'),
            dict(name='m', desc='数词', color='#929f24'),
            dict(name='q', desc='量词', color='#58089c'),
            dict(name='d', desc='副词', color='#2e6bbe'),
            dict(name='p', desc='介词', color='#2f54eb'),
            dict(name='c', desc='连词', color='#531dab'),
            dict(name='u', desc='助词', color='#7cb305'),
            dict(name='e', desc='叹词', color='#13c2c2'),
            dict(name='y', desc='语气词', color='#9e330d'),
            dict(name='o', desc='拟声词', color='#8c11f3'),
            dict(name='h', desc='前缀', color='#ee8311'),
            dict(name='k', desc='后缀', color='#08709c'),
            dict(name='w', desc='标点符号', color='#0da3d4'),
            dict(name='Ag', desc='形语素', color='#089c82'),
            dict(name='ad', desc='副形词', color='#089c82'),
            dict(name='An', desc='名形词', color='#089c82'),
            dict(name='Bg', desc='区别语素', color='#089c82'),
            dict(name='Dg', desc='副语素', color='#089c82'),
            dict(name='g', desc='语素', color='#089c82'),
            dict(name='i', desc='成语', color='#089c82'),
            dict(name='j', desc='简略词', color='#089c82'),
            dict(name='l', desc='习用语', color='#089c82'),
            dict(name='Mg', desc='数语素', color='#089c82'),
            dict(name='Ng', desc='名语素', color='#089c82'),
            dict(name='nx', desc='外文字符', color='#089c82'),
            dict(name='Qg', desc='量语素', color='#089c82'),
            dict(name='Rg', desc='代语素', color='#089c82'),
            dict(name='Tg', desc='时间语素', color='#089c82'),
            dict(name='Ug', desc='助语素', color='#089c82'),
            dict(name='Vg', desc='动语素', color='#089c82'),
            dict(name='vd', desc='副动词', color='#089c82'),
            dict(name='vn', desc='名动词', color='#089c82'),
            dict(name='x', desc='非语素词', color='#089c82'),
            dict(name='Yg', desc='语气语素', color='#089c82'),
        ]

        for i in range(len(doc_terms)):
            doc_terms[i]['index'] = i + 1
        return doc_terms

    @staticmethod
    def check_job_type_by_files(files):
        """检查任务类型"""
        ext_sets = set([get_ext(f.filename) for f in files])
        if ext_sets.issubset(('pdf', 'doc', 'docx')):
            job_type = 'e_doc'
        elif ext_sets.issubset(('txt', 'csv')):
            job_type = 'text'
        else:
            job_type = ''
        return job_type

    @staticmethod
    def tuple_list2dict(t):
        """convert 3 element tuple to a nested dict"""
        dict = {}
        for a, b, c in t:
            if a in dict:
                if b not in dict[a]:
                    dict[a][b] = c
            else:
                dict[a] = {b: c}
        return dict

    @staticmethod
    def order_by_model_fields(q, model, fields):
        for field in fields:
            if field[0] in ('+', '-'):
                flag = field[0]
                attr_name = field[1:]
            else:
                flag = '+'
                attr_name = field
            order = {'+': 'asc', '-': 'desc'}[flag]
            attr = getattr(model, attr_name)
            condition = getattr(attr, order)()
            q = q.order_by(condition)
        return q

    @staticmethod
    def check_doc_term_include(s_list, key, d_list):
        for s in s_list:
            for d in d_list:
                if isinstance(s, dict) and s.get(key) == d:
                    return True
        return False

    @staticmethod
    def check_doc_relation_include(s_list, key, d_list):
        for s in s_list:
            for d in d_list:
                if isinstance(s, dict) and s.get(key) == d:
                    return True
        return False

    @staticmethod
    def restore_sentence(sentence):
        result_sentence = ""
        for p in sentence.split("  "):
            result_sentence += p.rsplit("/", maxsplit=1)[0]
        return result_sentence
