# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/3/12
import os
import json
import datetime


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
