import typing

from app.common.common import RoleEnum, StatusEnum
from app.common.filters import CurrentUser
from app.model import DocTypeModel, TrainJobModel, MarkJobModel


class DashboardService:
    @staticmethod
    def get_dashboard_stats(result_skeleton, current_user: CurrentUser):
        # Step 1. 获取项目数量(doc_type)
        # doc_type_count_by_nlp_tasks = DocTypeModel().count_doc_type_by_nlp_task(current_user)
        # Step 2. 获取模型数量(train_job)
        train_job_count_by_nlp_tasks: typing.List = []
        if current_user.user_role in [RoleEnum.admin.value, RoleEnum.manager.value, RoleEnum.guest.value]:
            train_job_count_by_nlp_tasks = TrainJobModel().count_train_job_by_nlp_task(current_user)
        # Step 3. 获取各项目所有标注数、已标注任务数量、已审核+已标注任务数量(mark_job)
        # sample result: [(5(count),1(nlp_task_id),1(doc_type_id),6(status_id))]
        mark_job_count_by_nlp_tasks = MarkJobModel().count_mark_job_by_nlp_task(current_user)
        # Step 4. Compose result
        for r in result_skeleton:
            doc_type_list = []
            mark_job_count, labeled_count, reviewed_count = 0, 0, 0
            for row in mark_job_count_by_nlp_tasks:
                if row[1] == r["nlp_task_id"]:
                    mark_job_count += row[0]
                    if row[2] not in doc_type_list:
                        doc_type_list.append(row[2])
                    if row[3] in [StatusEnum.approved.value]:
                        reviewed_count += row[0]
                        labeled_count += row[0]
                    if row[3] in [StatusEnum.labeled.value]:
                        labeled_count += row[0]
            r["doc_type_number"] = len(doc_type_list)
            r["mark_job_number"] = mark_job_count
            r["labeled_number"] = labeled_count
            r["audited_number"] = reviewed_count

            if current_user.user_role in [RoleEnum.admin.value, RoleEnum.manager.value, RoleEnum.guest.value]:
                train_job_count = [c for c in train_job_count_by_nlp_tasks if c[0] == r["nlp_task_id"]] or [(0, 0)]
                r["model_number"] = train_job_count[0][1]
        return result_skeleton

    @staticmethod
    def dashboard_stats_reviewer_annotator(result_skeleton, current_user: CurrentUser):
        """
        标注员审核员只能看assign给自己的任务，只统计mark_job
        """
        all_mark_job_count_by_nlp_task = MarkJobModel().count_mark_job_by_nlp_task(current_user)
        return result_skeleton
