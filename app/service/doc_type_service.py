# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/30-10:58 上午
from app.common.common import StatusEnum, NlpTaskEnum
from app.common.extension import session
from app.common.filters import CurrentUser
from app.model import DocTypeModel, MarkTaskModel
from app.model.doc_term_model import DocTermModel
from app.model.evaluate_task_model import EvaluateTaskModel
from app.schema.doc_type_schema import DocTypeSchema, DocTermSchema, EntityDocTypeSchema, WordsegDocTypeSchema
from app.schema.evaluate_task_schema import EvaluateTaskSchema


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
        doc_type_list = [{"doc_type": DocTypeSchema().dump(d)} for d in doc_type_list]

        # get all job count and approved job count
        all_status, all_marked_status = MarkTaskModel().count_status_by_user(nlp_task_id=nlp_task_id, current_user=current_user)

        # calculate marked mark_job count and all mark_job for each doc_type
        all_status_dict = {_doc_type_id: {_mark_job_id: _count_sum} for _doc_type_id, _mark_job_id, _count_sum in all_status}
        all_marked_status_dict = {_doc_type_id: {_mark_job_id: _count_sum} for _doc_type_id, _mark_job_id, _count_sum in all_marked_status}
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
            latest_evaluate = EvaluateTaskModel().get_latest_evaluate_by_doc_type_id(nlp_task_id=nlp_task_id, doc_type_id=doc_type_id)
            if latest_evaluate:
                latest_evaluate.evaluate_task_status = StatusEnum(latest_evaluate.evaluate_task_status).name
                doc_type.update(evaluate=EvaluateTaskSchema().dump(latest_evaluate))
            result.append(doc_type)
        return result

    @staticmethod
    def get_doc_type(current_user: CurrentUser, args):
        mark_job_ids = args.get('mark_job_ids', [])
        count, items = DocTypeModel().get_by_mark_job_ids(mark_job_ids=mark_job_ids, nlp_task_id=args["nlp_task_id"], current_user=current_user, offset=args["offset"], limit=args["limit"])
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
        if args.get("nlp_task_id") == NlpTaskEnum.wordseg:
            result = WordsegDocTypeSchema().dumps(doc_type)
        elif args.get("nlp_task_id") == NlpTaskEnum.relation:
            result = EntityDocTypeSchema().dumps(doc_type)
        else:
            result = DocTypeSchema().dumps(doc_type)
        return result

    @staticmethod
    def set_favoriate_doc_type(doc_type_id, is_favorite: bool):
        _doc_type = DocTypeModel().update(doc_type_id=doc_type_id, is_favorite=is_favorite)
        return DocTypeSchema().dump(_doc_type)

    @staticmethod
    def get_doc_type_items(doc_type_id: int):
        item = DocTermModel().get_by_filter(doc_type_id=doc_type_id)
        return DocTermSchema().dump(item)

    @staticmethod
    def delete_doc_type(doc_type_id):
        DocTypeModel().delete(doc_type_id)
        session.commit()

    @staticmethod
    def update_doc_type(args, doc_type_id):
        item = DocTypeModel().update(doc_type_id, **args)
        if args.get("doc_term_list"):
            for i in args.get("doc_term_list"):
                i.update({"doc_type_id": doc_type_id})
            DocTermModel().bulk_update(args.get("doc_term_list"))
        session.commit()

        return DocTypeSchema().dump(item)

    @staticmethod
    def check_doc_type_name_exists(doc_type_name):
        return DocTypeModel().if_exists_by_name(doc_type_name)
