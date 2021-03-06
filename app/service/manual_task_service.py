# -*- coding:utf-8 -*-  
""" 
@Author:guochuanxiang 
@File: manual_task_service.py 
@Time: 2020/04/11 14:00
@Email: guochuanxiang@datagrand.com
@IDE: PyCharm 
"""
from app.common.common import NlpTaskEnum, RoleEnum, StatusEnum
from app.common.filters import CurrentUser
from app.common.utils.status_mapper import status_str2int_mapper
from app.model import MarkTaskModel, MarkJobModel, UserTaskModel
from app.common.extension import session
from app.schema import MarkTaskSchema, UserTaskSchema

nlp_task_mapper = {
    "mark": int(NlpTaskEnum.extract),
    "classify_mark": int(NlpTaskEnum.classify),
    "relation_mark": int(NlpTaskEnum.relation),
    "wordseg_mark": int(NlpTaskEnum.wordseg),
    "extract": int(NlpTaskEnum.extract),
    "classify_extract": int(NlpTaskEnum.classify),
    "relation_extract": int(NlpTaskEnum.relation),
    "wordseg_extract": int(NlpTaskEnum.wordseg),
}


class ManualTaskService:
    @staticmethod
    def detele_task(task_id):
        mark_job_id = MarkTaskModel().get_mark_job_id_by_id(task_id)
        MarkTaskModel().delete(task_id)
        session.commit()
        mark_job_status = MarkJobModel().check_mark_job_status(mark_job_id)
        mark_job = MarkJobModel().update(mark_job_id, **{'mark_job_status': mark_job_status})
        session.commit()
        return mark_job

    @staticmethod
    def reject_mark_task(mark_task_id):
        UserTaskModel().update_status_to_unlabel_by_mark_task_id(mark_task_id)
        MarkTaskModel().update_status_to_unlabel_by_mark_task_id(mark_task_id)
        session.commit()

    @staticmethod
    def get_user_task_or_mark_task_result_by_role(current_user: CurrentUser, args):
        nlp_task_id = nlp_task_mapper.get(args['job_type'])
        if current_user.user_role in [RoleEnum.annotator.value]:
            count, processed, items = UserTaskModel().get_user_task_with_doc_and_doc_type(nlp_task_id=nlp_task_id,
                                                                                          current_user=current_user,
                                                                                          args=args)
            schema = UserTaskSchema
        else:
            count, processed, items = MarkTaskModel().get_mark_task_with_doc_and_doc_type(nlp_task_id=nlp_task_id,
                                                                                          current_user=current_user,
                                                                                          args=args)
            schema = MarkTaskSchema
        if args['job_type'] == 'classify_mark':
            # TODO 返回数据格式转换
            result = schema(many=True).dump(items)
        else:
            result = schema(many=True, exclude=('task_result',)).dump(items)
        return count, processed, result

    @staticmethod
    def update_mark_task_or_user_task_status(current_user: CurrentUser, task_id, args):
        if current_user.user_role in [RoleEnum.annotator.value]:
            if args.get('task_result'):
                args['user_task_result'] = args.get('task_result')
                del args['task_result']
            if args.get('task_state'):
                args['user_task_status'] = int(getattr(StatusEnum, args['task_state']))
                del args['task_state']
            item = UserTaskModel().update_by_annotator_id(current_user, task_id, **args)
            MarkTaskModel().check_user_task_and_update_mark_task(task_id)
            schema = UserTaskSchema
        else:
            if args.get('task_result'):
                args['mark_task_result'] = args.get('task_result')
                del args['task_result']
            if args.get('task_state'):
                args['mark_task_status'] = int(getattr(StatusEnum, args['task_state']))
                del args['task_state']
            item = MarkTaskModel().update(task_id, **args)
            schema = MarkTaskSchema

        session.commit()
        result = schema().dump(item)
        return result

    @staticmethod
    def update_user_task_status(current_user: CurrentUser, task_id, args):
        if args.get('task_result'):
            args['user_task_result'] = args.get('task_result')
            del args['task_result']
        if args.get('task_state'):
            args['user_task_status'] = status_str2int_mapper()[args['task_state']]
            del args['task_state']
        item = UserTaskModel().update_by_annotator_id(current_user, task_id, **args)
        MarkTaskModel().check_user_task_and_update_mark_task(task_id)
        schema = UserTaskSchema
        session.commit()
        result = schema().dump(item)
        return result

    @staticmethod
    def update_mark_task_status(current_user: CurrentUser, task_id, args):
        if args.get('task_result'):
            args['mark_task_result'] = args.get('task_result')
            del args['task_result']
        if args.get('task_state'):
            args['mark_task_status'] = status_str2int_mapper()[args['task_state']]
            del args['task_state']
        item = MarkTaskModel().update(task_id, **args)
        schema = MarkTaskSchema
        session.commit()
        result = schema().dump(item)
        return result

    @staticmethod
    def get_mark_task_or_user_task(current_user: CurrentUser, task_id: int):
        """

        :param current_user:
        :param task_id: 如果是标注员则为user task id 如果是审核员员则为mark task id
        :return:
        """
        if current_user.user_role in [RoleEnum.annotator.value]:
            item = UserTaskModel().get_user_task_with_doc_and_user_task_list_by_id(task_id)
            schema = UserTaskSchema
        else:
            item = MarkTaskModel().get_mark_task_with_doc_and_user_task_list_by_id(task_id)
            schema = MarkTaskSchema
        result = schema().dump(item)
        return result

    @staticmethod
    def get_preview_and_next_task_id(current_user: CurrentUser, task_id, args):
        nlp_task_id = nlp_task_mapper.get(args['job_type'])
        if current_user.user_role in [RoleEnum.annotator.value]:
            preview_task_id, next_task_id = UserTaskModel().get_preview_and_next_user_task_id(current_user, nlp_task_id, task_id, args)
        else:
            preview_task_id, next_task_id = MarkTaskModel().get_preview_and_next_mark_task_id(current_user, nlp_task_id, task_id, args)
        return preview_task_id, next_task_id

    @staticmethod
    def export_pdf(task_id):
        doc_unique_name, doc_raw_name, labels = MarkTaskModel().get_doc_and_lable(task_id)
        return doc_unique_name, doc_raw_name, labels
