# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/30-10:58 上午
import typing

from app.common.common import Common
from app.common.extension import session
from app.common.filters import CurrentUser
from app.model import DocTypeModel, MarkTaskModel
from app.model.doc_relation_model import DocRelationModel
from app.model.doc_term_model import DocTermModel
from app.model.evaluate_task_model import EvaluateTaskModel
from app.model.wordseg_lexicon_model import WordsegLexiconModel
from app.schema import DocTypeSchema, EvaluateTaskSchema, WordsegDocLexiconSchema


class DocTypeService:
    @staticmethod
    def get_by_id(doc_type_id):
        doc_type = DocTypeModel().get_by_id(doc_type_id)
        return doc_type

    @staticmethod
    def get_by_id_by_user_group(doc_type_id, group_id):
        doc_type = DocTypeModel().get_by_id_by_user_group(_id=doc_type_id, group_id=group_id)
        return doc_type

    @staticmethod
    def get_doc_type_info_by_nlp_task_by_user(nlp_task_id, current_user):
        """
        获取管理大厅首页的doc_type信息
        """
        result = []
        # get doc_type list by user
        _, doc_type_list = DocTypeModel().get_by_nlp_task_id_by_user(nlp_task_id=nlp_task_id, current_user=current_user)
        for doc_type, terms in doc_type_list:
            doc_type.doc_terms = [int(t) for t in terms.split(",")] if terms is not None else []
        doc_type_list = [d[0] for d in doc_type_list]
        doc_type_list = [{"doc_type": DocTypeSchema().dump(doc_type)} for doc_type in doc_type_list]

        # get all job count and approved job count
        all_status, all_marked_status = MarkTaskModel().count_status_by_user(nlp_task_id=nlp_task_id, current_user=current_user)

        # calculate marked mark_job count and all mark_job for each doc_type
        all_status_dict = Common().tuple_list2dict(all_status)
        all_marked_status_dict = Common().tuple_list2dict(all_marked_status)

        for doc_type in doc_type_list:
            doc_type_id = doc_type["doc_type"]["doc_type_id"]
            mark_job_count = len(all_status_dict.get(doc_type_id, {}))
            marked_mark_job_count = 0
            for _mark_job_id, _count_sum in all_status_dict.get(doc_type_id, {}).items():
                if _count_sum == all_marked_status_dict.get(doc_type_id, {}).get(_mark_job_id, 0):
                    marked_mark_job_count += 1
            doc_type.update(progress_state={"job_num": mark_job_count,
                                            "labeled_job_number": marked_mark_job_count,
                                            "progress_rate": round(marked_mark_job_count / mark_job_count, 2) if mark_job_count > 0 else 0})

            # get latest evaluation result if exists
            latest_evaluate = EvaluateTaskModel().get_latest_evaluate_by_doc_type_id(nlp_task_id=nlp_task_id,
                                                                                     doc_type_id=doc_type_id)
            if latest_evaluate:
                doc_type.update(evaluate=EvaluateTaskSchema().dump(latest_evaluate))
            result.append(doc_type)
        return result

    @staticmethod
    def get_doc_type(current_user: CurrentUser, args):
        mark_job_ids = args.get('mark_job_ids', [])
        nlp_task_id = args["nlp_task_id"]
        count, items = DocTypeModel().get_by_mark_job_ids(mark_job_ids=mark_job_ids, nlp_task_id=nlp_task_id,
                                                          current_user=current_user, offset=args["offset"],
                                                          limit=args["limit"])
        result = DocTypeSchema(many=True).dump(items)
        return result, count

    @staticmethod
    def create_doc_type(current_user: CurrentUser, args):
        doc_term_list = args.pop('doc_term_list')
        if 'group_id' not in args or args['group_id'] < 1:
            args['group_id'] = current_user.user_groups[0]
        doc_type = DocTypeModel().create(**args)
        for item in doc_term_list:
            item.update({'doc_type_id': doc_type.doc_type_id})
        doc_type.doc_term_list = DocTermModel().bulk_create(doc_term_list)
        session.commit()
        result = DocTypeSchema().dumps(doc_type)
        return result

    @staticmethod
    def set_favoriate_doc_type(doc_type_id, is_favorite: bool):
        _doc_type = DocTypeModel().update(doc_type_id=doc_type_id, is_favorite=is_favorite)
        return DocTypeSchema().dump(_doc_type)

    @staticmethod
    def get_doc_type_items(doc_type_id: int):
        item = DocTypeModel().get_by_id(doc_type_id)
        item.doc_term_list = DocTermModel().get_by_filter(doc_type_id=doc_type_id)

        return DocTypeSchema().dump(item)

    @staticmethod
    def delete_doc_type(doc_type_id):
        DocTypeModel().delete(doc_type_id)
        session.commit()

    @staticmethod
    def update_relation_doc_type(args, doc_type_id):
        item = DocTypeModel().update(doc_type_id, **args)
        session.commit()
        return DocTypeSchema().dump(item)

    @staticmethod
    def update_doc_type(args, doc_type_id):
        item = DocTypeModel().update(doc_type_id, **args)
        existed_doc_term_ids = [dt.doc_term_id for dt in DocTermModel().get_by_filter(doc_type_id=doc_type_id)]
        updated_doc_term_ids = []
        if args.get("doc_term_list"):
            for i in args.get("doc_term_list"):
                i.update({"doc_type_id": doc_type_id})
                updated_doc_term_ids.append(i.get("doc_term_id", 0))
            DocTermModel().bulk_update(args.get("doc_term_list"))
        session.commit()

        # Remove doc terms
        for i in existed_doc_term_ids:
            if i not in updated_doc_term_ids:
                DocTermModel().delete(i)
        session.commit()
        return DocTypeSchema().dump(item)

    @staticmethod
    def check_doc_type_name_exists(doc_type_name):
        return DocTypeModel().if_exists_by_name(doc_type_name)

    @staticmethod
    def get_relation_list(doc_type_id: int, offset: int, limit: int, doc_relation_ids=[]):
        relations, count = DocRelationModel().get_relation_with_terms(offset=offset, limit=limit, require_count=True,
                                                                      doc_type_id=doc_type_id,
                                                                      doc_relation_ids=doc_relation_ids)

        result = [{"doc_relation_name": r[1], "doc_term_ids": [int(i) for i in r[3].split(",")],
                   "doc_relation_id":r[0]} for r in relations]
        return result, count

    @staticmethod
    def create_relation(doc_type_id: int, doc_term_ids: typing.List, doc_relation_name: str):
        if not DocTypeModel().get_by_id(doc_type_id):
            raise ValueError(f"DocType {doc_type_id} 不存在")
        if len(DocTermModel().get_by_filter(doc_term_ids=doc_term_ids)) != 2:
            raise ValueError(f"DocTerm 不存在或已被删除")

        item = DocTermModel().create_relation(doc_relation_name, doc_term_ids, doc_type_id=doc_type_id)
        session.commit()
        return {
            "doc_relation_name": doc_relation_name,
            "doc_relation_id": item.doc_relation_id
        }

    @staticmethod
    def delete_relation(doc_relation_id):
        DocTermModel().delete_relation_mapping(doc_relation_id)
        DocTermModel().delete_relation(doc_relation_id)
        session.commit()

    @staticmethod
    def update_relation(doc_type_id, doc_relation_name, doc_term_ids):
        # _, item = session.query(EntityDocType, EntityDocRelation).filter(
        #     EntityDocType.doc_type_id == doc_type_id,
        #     EntityDocType.status,
        #     EntityDocRelation.doc_type_id == EntityDocType.doc_type_id,
        #     EntityDocRelation.doc_relation_id == doc_relation_id,
        #     EntityDocRelation.status,
        # ).one()
        # doc_relation_term_items = session.query(EntityDocRelationTerm).filter(
        #     EntityDocRelationTerm.doc_relation_id == doc_relation_id
        # ).all()
        # for index, doc_relation_term_item in enumerate(doc_relation_term_items):
        #     doc_relation_term_item.status = False
        #
        #     if index <= len(doc_term_ids):
        #         doc_relation_term_item.doc_term_id = doc_term_ids[index]
        #         doc_relation_term_item.status = True
        #
        # item.update(**args)
        # session.commit()
        # result = EntityDocTermSchema().dump(item)
        return None

    @staticmethod
    def create_relation_doc_type(args):
        item = DocTypeModel().create(**args)
        session.commit()
        result = DocTypeSchema().dump(item)
        return result

    @staticmethod
    def get_wordseg_lexicon(doc_type_id, offset, limit):
        items, count = WordsegLexiconModel().get_by_filter(doc_type_id=doc_type_id, offset=offset, limit=limit)
        result = WordsegDocLexiconSchema(many=True).dump(items)
        return result

    @staticmethod
    def create_wordseg_lexicon(doc_type_id, kwargs):
        kwargs.update({"doc_type_id": doc_type_id})
        item = WordsegLexiconModel().create(**kwargs)
        result = WordsegDocLexiconSchema().dump(item)
        return result

