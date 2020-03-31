from app.model import DocTypeModel, TrainJobModel, MarkJobModel


class DashboardService:
    @staticmethod
    def get_dashboard_stats_manager(result_skeleton, user_id):
        # Step 1. 获取项目数量(doc_type)
        doc_type_count_by_nlp_tasks = DocTypeModel().count_doc_type_by_nlp_task_manager(user_id)
        # Step 2. 获取模型数量(train_job)
        train_job_count_by_nlp_tasks = TrainJobModel().count_train_job_by_nlp_task(user_id)
        # Step 3. 获取各项目所有标注数、已标注任务数量、已审核+已标注任务数量(mark_job)
        all_mark_job_count_by_nlp_task, labeled_mark_job_count_by_nlp_task, reviewed_mark_job_count_by_nlp_task = \
            MarkJobModel().count_mark_job_by_nlp_task_manager(user_id)
        # Step 4. Compose result
        for r in result_skeleton:
            doc_type_count = [c for c in doc_type_count_by_nlp_tasks if c[0] == r["nlp_task_id"]] or [(0, 0)]
            r["doc_type_number"] = doc_type_count[0][1]
            train_job_count = [c for c in train_job_count_by_nlp_tasks if c[0] == r["nlp_task_id"]] or [(0, 0)]
            r["model_number"] = train_job_count[0][1]
            all_mark_job_count = [c for c in all_mark_job_count_by_nlp_task if c[0] == r["nlp_task_id"]] or [(0, 0)]
            r["mark_job_number"] = all_mark_job_count[0][1]
            labeled_mark_job_count = [c for c in labeled_mark_job_count_by_nlp_task if c[0] == r["nlp_task_id"]] or [
                (0, 0)]
            r["labeled_number"] = labeled_mark_job_count[0][1]
            reviewed_mark_job_count = [c for c in reviewed_mark_job_count_by_nlp_task if c[0] == r["nlp_task_id"]] or [
                (0, 0)]
            r["audited_number"] = reviewed_mark_job_count[0][1]
        return result_skeleton

    @staticmethod
    def dashboard_stats_reviewer_annotator(result_skeleton, user_id):
        """
        标注员审核员只能看assign给自己的任务，只统计mark_job
        """
        all_mark_job_count_by_nlp_task = MarkJobModel().count_mark_job_by_nlp_task_reviewer(user_id)
        return result_skeleton
