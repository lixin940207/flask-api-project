# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: doc_type_service.py 
@Time: 2020/03/26 16:56
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
import json
import time

from app.common.extension import session
from app.common.log import logger
from app.common.redis import r
from app.model import DocTermModel
from app.model.classify_rule_model import ClassifyRuleModel
from app.model.wordseg_lexicon_model import WordsegLexiconModel
from app.schema import DocTermSchema, WordsegDocLexiconSchema
from app.schema.doc_type_schema import ClassifyDocRuleSchema


class DocTermService:
    @staticmethod
    def get_doc_term_list(args):
        exclude_terms_ids = args.get('exclude_terms_ids', [])
        offset = args.get('offset', 0)
        limit = args.get('limit', 10)
        items, count = DocTermModel().get_by_exclude_terms(exclude_terms_ids=exclude_terms_ids, offset=offset,
                                                           limit=limit)
        result = DocTermSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def get_doc_term_by_doctype(doc_type_id, offset=0, limit=10, doc_term_ids=None):
        items, count = DocTermModel().get_doc_term_by_doctype(doc_type_id, offset, limit, doc_term_ids)
        result = DocTermSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def create_doc_term(args, doc_type_id):
        item = DocTermModel().create(**args, doc_type_id=doc_type_id)
        session.commit()
        result = DocTermSchema().dump(item)
        return result

    @staticmethod
    def create_classify_doc_term(args, doc_type_id, doc_rule_list):
        doc_term = DocTermModel().create(**args, doc_type_id=doc_type_id)
        doc_term.flush()
        for doc_rule_dict in doc_rule_list:
            ClassifyRuleModel().create(doc_term_id=doc_term.doc_term_id, **doc_rule_dict)
        session.commit()
        result = DocTermSchema().dump(doc_term)
        return result

    @staticmethod
    def check_term_in_relation(doc_term_id):
        return DocTermModel().check_term_in_relation(doc_term_id)

    @staticmethod
    def remove_doc_term(doc_term_id):
        DocTermModel().delete(doc_term_id)

    @staticmethod
    def update_doc_term(doc_term_id, args):
        item = DocTermModel().update(doc_term_id, **args)
        session.commit()
        result = DocTermSchema().dump(item)
        return result

    @staticmethod
    def get_wordseg_lexicon(doc_type_id, offset, limit):
        items, count = WordsegLexiconModel().get_by_filter(doc_type_id=doc_type_id, offset=offset, limit=limit,
                                                           require_count=True)
        result = WordsegDocLexiconSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def create_wordseg_lexicon(kwargs):
        item = WordsegLexiconModel().create(**kwargs)
        session.commit()
        result = WordsegDocLexiconSchema().dump(item)
        return result

    @staticmethod
    def get_wordseg_lexicon_item(doc_lexicon_id):
        doc_lexicon = WordsegLexiconModel().get_by_id(doc_lexicon_id)
        session.commit()
        result = WordsegDocLexiconSchema().dump(doc_lexicon)
        return result

    @staticmethod
    def delete_wordseg_lexicon_by_id(doc_lexicon_id):
        WordsegLexiconModel().delete(doc_lexicon_id)
        session.commit()

    @staticmethod
    def update_wordseg_lexicon(doc_lexicon_id, args):
        item = WordsegLexiconModel().update(doc_lexicon_id, **args)
        session.commit()
        result = WordsegDocLexiconSchema().dump(item)
        return result

    @staticmethod
    def get_classify_doc_rule(doc_type_id, offset, limit):
        items, count = DocTermModel().get_classify_doc_rule(doc_type_id, offset, limit)
        result = ClassifyDocRuleSchema(many=True).dump(items)
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return result, count, timestamp

    @staticmethod
    def create_new_rule(args):
        is_existed = DocTermModel().check_exists_rule(args.get("doc_term_id"))
        if is_existed:
            raise ValueError("该标签的规则已存在，请勿重复创建")
        classify_rule = DocTermModel().create_classify_rule(**args)
        session.commit()
        result = ClassifyDocRuleSchema().dump(classify_rule)
        return result

    @staticmethod
    def get_classify_rule(doc_rule_id):
        doc_rule = ClassifyRuleModel().get_by_id(doc_rule_id)
        doc_rule = ClassifyDocRuleSchema().dump(doc_rule)
        return doc_rule

    @staticmethod
    def update_classify_rule(args, doc_rule_id):
        doc_rule = ClassifyRuleModel().update(doc_rule_id, **args)
        doc_rule = ClassifyDocRuleSchema().dump(doc_rule)
        return doc_rule

    @staticmethod
    def delete_doc_rule(doc_rule_id):
        ClassifyRuleModel().delete(doc_rule_id)
        session.commit()

    @staticmethod
    def update_rule_to_redis(doc_type_id: int) -> None:
        rule_mapper = {}
        rule_and_terms = ClassifyRuleModel().get_rule_with_term(doc_type_id)
        for doc_rule, doc_term in rule_and_terms:
            rule_mapper[doc_term.doc_term_id] = doc_rule.rule_content

        r.set(f'queue:rule:{doc_type_id}', json.dumps(rule_mapper))
        r.set(f'queue:time:{doc_type_id}', time.strftime("%Y%m%d%H%M%S", time.localtime()))
        logger.info(rule_mapper)  # 开发调试

