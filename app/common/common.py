# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
import os
import json
import datetime
from flask_restful import request

from app.common.seeds import NlpTaskEnum


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
    def get_nlp_task_id(args):
        nlp_task_url = request.url.split('/')[-1]
        if 'classify' in nlp_task_url:
            nlp_task_id = int(getattr(NlpTaskEnum, 'classify'))
        elif 'entity' in nlp_task_url:
            nlp_task_id = int(getattr(NlpTaskEnum, 'relation'))
        elif 'wordseg' in nlp_task_url:
            nlp_task_id = int(getattr(NlpTaskEnum, 'wordseg'))
        else:
            nlp_task_id = int(getattr(NlpTaskEnum, 'extract'))
        args.update({
            'nlp_task_id': nlp_task_id
        })
