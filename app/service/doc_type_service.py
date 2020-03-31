# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/3/30-10:58 上午
from app.common.extension import session
from app.common.filters import CurrentUser
from app.common.seeds import NlpTaskEnum
from app.model import DocTypeModel, MarkTaskModel
from app.model.doc_term_model import DocTermModel
from app.model.evaluate_task_model import EvaluateTaskModel
from app.schema.doc_type_schema import DocTypeSchema
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
    def get_doc_type_info_by_nlp_task_by_user(nlp_task, current_user):
        result = []
        nlp_task_id = int(getattr(NlpTaskEnum, nlp_task))

        # get doc_type list by user role and user id
        doc_type_list = DocTypeModel().get_by_nlp_task_id_by_user(nlp_task_id=nlp_task_id, )
        doc_type_list = [{"doc_type": DocTypeSchema().dump(d)} for d in doc_type_list]
        # get all job count and approved job count
        all_status, all_finish_marking_status = MarkTaskModel().count_status_by_user(nlp_task_id=nlp_task_id, current_user=current_user)

        # iterate doc_type list to calculate their progress state
        for item in doc_type_list:
            doc_type_id = item["doc_type"]["doc_type_id"]
            mark_job_count = 0
            marked_mark_job_count = 0
            for i in range(len(all_status)):
                if all_status[i][0] == doc_type_id:
                    mark_job_count += 1
                    mark_job_id = all_status[i][1]
                    count_sum = all_status[i][2]
                    for j in range(len(all_finish_marking_status)):
                        if all_finish_marking_status[j][0] == doc_type_id \
                                and all_finish_marking_status[j][1] == mark_job_id \
                                and all_finish_marking_status[j][2] == count_sum:
                            marked_mark_job_count += 1
                            break
            item.update(progress_state={"job_num": mark_job_count, "labeled_job_number": marked_mark_job_count,
                                        "progress_rate": round(marked_mark_job_count / mark_job_count,
                                                               2) if mark_job_count > 0 else 0})
            # get latest evaluation result if exists
            latest_evaluate = EvaluateTaskModel().get_latest_evaluate_by_doc_type_id(nlp_task=nlp_task, doc_type_id=doc_type_id)
            if latest_evaluate:
                item.update(evaluate=EvaluateTaskSchema().dump(latest_evaluate))
            result.append(item)
        return result

    def get_doc_type(current_user: CurrentUser, args):
        offset = args.get('offset', 0)
        limit = args.get('limit', 10)
        mark_job_ids = args.get('mark_job_ids', [])
        nlp_task_id = args.get('nlp_task_id')
        items, count = DocTypeModel().get_by_mark_job_ids(mark_job_ids=mark_job_ids, nlp_task_id=nlp_task_id, current_user=current_user, offset=offset, limit=limit)
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
