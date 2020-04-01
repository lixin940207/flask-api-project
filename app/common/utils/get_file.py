import json
from app.config.config import ROOT_PATH


def get_csv(path):
    with open(ROOT_PATH / path) as f:
        data = f.read()
        # TODO process csv
    return data


def get_json(path):
    with open(ROOT_PATH / path) as f:
        data = json.loads(f.read())
    return data
