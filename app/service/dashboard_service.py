import pydash
from app.model.doc_type_model import DocTypeModel
from app.common.seeds import NlpTaskEnum, StatusEnum


class DashboardService:
    @staticmethod
    def get_dashboard_stats_manager():
        result = [
            {"type": "分类项目", "nlp_task_id": int(NlpTaskEnum.classify)},
            {"type": "抽取项目", "nlp_task_id": int(NlpTaskEnum.extract)},
            {"type": "实体关系", "nlp_task_id": int(NlpTaskEnum.relation)},
            {"type": "分词项目", "nlp_task_id": int(NlpTaskEnum.wordseg)},
        ]
        # Step 1. 获取项目数量(doc_type)
        all_doc_types = DocTypeModel().count_doc_type_by_nlp_task()

        # Step 2. 获取模型数量(train_job)
        # Step 3. 获取各项目所有标注数(mark_job)
        # Step 3. 获取各项目已标注任务数量(mark_job)
        # Step 4. 获取各项目已审核+已标注任务数量(mark_job)


    @staticmethod
    def dashboard_stats_review_annotator():
        pass

