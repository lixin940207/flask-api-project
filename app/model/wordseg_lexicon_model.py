# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/14
from abc import ABC
from app.entity.wordseg_lexicon import WordsegDocLexicon
from app.model.base import BaseModel
from app.common.extension import session


class WordsegLexiconModel(BaseModel, ABC):
    def get_all(self):
        pass

    def get_by_id(self, _id):
        pass

    def get_by_filter(self, search=None, order_by="created_time", order_by_desc=True, limit=10, offset=0, require_count=False
                      , **kwargs):
        accept_keys = ["doc_type_id"]
        q = session.query(WordsegDocLexicon).filter(~WordsegDocLexicon.is_deleted)
        for key, val in kwargs.items():
            if key in accept_keys:
                q = q.filter(getattr(WordsegDocLexicon, key) == val)
        count = 0
        if require_count:
            count = q.count()
        # Descending order
        if order_by_desc:
            q = q.order_by(getattr(WordsegDocLexicon, order_by).desc())
        else:
            q = q.order_by(getattr(WordsegDocLexicon, order_by))
        q = q.offset(offset).limit(limit)

        return q.all(), count

    def create(self, **kwargs):
        entity = WordsegDocLexicon(**kwargs)
        session.add(entity)
        session.flush()
        return entity

    def bulk_create(self, entity_list):
        pass

    def delete(self, _id):
        pass

    def bulk_delete(self, _id_list):
        pass

    def bulk_delete_by_filter(self, **kwargs):
        pass

    def update(self, entity):
        pass

    def bulk_update(self, entity_list):
        pass
