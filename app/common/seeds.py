from app.common.log import logger
from app.common.extension import session
from enum import Enum


class NlpTaskEnum(int, Enum):
    extract = 1,
    classify = 2,
    wordseg = 3,
    relation = 4


class StatusEnum(int, Enum):
    init = 1,
    queueing = 2,
    processing = 3,
    unlabel = 4,
    labeling = 5,
    labeled = 6,
    reviewing = 7,
    approved = 8,
    fail = 9
    success = 10


class Seeds:
    def create_seeds(self):
        # Create seeds data from base tables
        self.create_nlp_task()
        self.create_status()
        self.create_doc_type()

    @staticmethod
    def create_nlp_task():
        from app.entity import NlpTask
        from app.model import NlpTaskModel
        if len(NlpTaskModel().get_all()) == 0:
            init_nlp_tasks = [
                NlpTask(app_id=1, created_by=1, nlp_task_id=NlpTaskEnum.extract, nlp_task_name="extract"),
                NlpTask(app_id=1, created_by=1, nlp_task_id=NlpTaskEnum.classify, nlp_task_name="classify"),
                NlpTask(app_id=1, created_by=1, nlp_task_id=NlpTaskEnum.wordseg, nlp_task_name="wordseg"),
                NlpTask(app_id=1, created_by=1, nlp_task_id=NlpTaskEnum.relation, nlp_task_name="relation"),
            ]
            NlpTaskModel().bulk_create(init_nlp_tasks)
            session.commit()
            logger.info(" [x] Seeds nlp_task has been created. ")

    @staticmethod
    def create_status():
        from app.entity import Status
        from app.model import StatusModel
        if len(StatusModel().get_all()) == 0:
            init_status = [
                Status(app_id=1, created_by=1, status_id=StatusEnum.init, status_name="init"),
                Status(app_id=1, created_by=1, status_id=StatusEnum.queueing, status_name="queueing"),
                Status(app_id=1, created_by=1, status_id=StatusEnum.processing, status_name="processing"),
                Status(app_id=1, created_by=1, status_id=StatusEnum.unlabel, status_name="unlabel"),
                Status(app_id=1, created_by=1, status_id=StatusEnum.labeled, status_name="labeled"),
                Status(app_id=1, created_by=1, status_id=StatusEnum.reviewing, status_name="reviewing"),    # auditing
                Status(app_id=1, created_by=1, status_id=StatusEnum.approved, status_name="approved"),     # audited
                Status(app_id=1, created_by=1, status_id=StatusEnum.fail, status_name="fail"),         # failed
                Status(app_id=1, created_by=1, status_id=StatusEnum.success, status_name="success"),
            ]
            StatusModel().bulk_create(init_status)
            session.commit()
            logger.info(" [x] Seeds status has been created. ")

    @staticmethod
    def create_doc_type():
        from app.entity import DocType
        from app.model import DocTypeModel
        if len(DocTypeModel().get_all()) == 0:
            doc_types = [
                DocType(app_id=1, created_by=1, doc_type_id=1, doc_type_name="测试抽取项目1", nlp_task_id=int(NlpTaskEnum.extract)),
                DocType(app_id=1, created_by=1, doc_type_id=2, doc_type_name="测试抽取项目2", nlp_task_id=int(NlpTaskEnum.extract)),
                DocType(app_id=1, created_by=1, doc_type_id=3, doc_type_name="测试抽取项目3", nlp_task_id=int(NlpTaskEnum.extract)),
                DocType(app_id=1, created_by=1, doc_type_id=4, doc_type_name="测试抽取项目4", nlp_task_id=int(NlpTaskEnum.extract)),
                DocType(app_id=1, created_by=1, doc_type_id=5, doc_type_name="测试分类项目1", nlp_task_id=int(NlpTaskEnum.classify)),
                DocType(app_id=1, created_by=1, doc_type_id=6, doc_type_name="测试分类项目2", nlp_task_id=int(NlpTaskEnum.classify)),
                DocType(app_id=1, created_by=1, doc_type_id=7, doc_type_name="测试分类项目3", nlp_task_id=int(NlpTaskEnum.classify)),
                DocType(app_id=1, created_by=1, doc_type_id=8, doc_type_name="测试关系项目1", nlp_task_id=int(NlpTaskEnum.relation)),
                DocType(app_id=1, created_by=1, doc_type_id=9, doc_type_name="测试关系项目2", nlp_task_id=int(NlpTaskEnum.relation)),
                DocType(app_id=1, created_by=1, doc_type_id=10, doc_type_name="测试分词项目1", nlp_task_id=int(NlpTaskEnum.wordseg)),
                DocType(app_id=1, created_by=1, doc_type_id=11, doc_type_name="测试分词项目2", nlp_task_id=int(NlpTaskEnum.wordseg)),
            ]
            DocTypeModel().bulk_create(doc_types)
            session.commit()

    @staticmethod
    def create_mark_job():
        from app.entity import MarkJob
        pass

    @staticmethod
    def create_train_job():
        pass
