# coding=utf-8
# @Author: Jiasheng Gu
# @Date: 2020/4/3
from app.common.extension import session
from app.model import DocModel


class DocService:
    @staticmethod
    def get_by_id(doc_id):
        doc = DocModel().get_by_id(doc_id)
        return doc

    @staticmethod
    def get_docs(args):
        filters = {}
        if args.get('doc_ids'):
            filters["doc_ids"] = args.get('doc_ids')
        elif args.get('doc_term_ids'):
            filters["doc_term_ids"] = args.get('doc_term_ids')
        elif args.get('mark_job_ids'):
            filters["mark_job_ids"] = args.get('doc_term_ids')
        return DocModel().get_by_filter(**filters)

    @staticmethod
    def update_doc_by_id(doc_id, args):
        doc = DocModel().update(doc_id, **args)
        session.commit()
        return doc
