from app.common.log import logger
from app.common.extension import session
from app.common.common import NlpTaskEnum, StatusEnum


class Seeds:
    def create_seeds(self):
        # Create seeds data from base tables
        self.create_nlp_task()
        self.create_status()
        self.create_doc_type()
        self.create_mark_job()
        self.create_train_job()
        self.create_doc()
        self.create_mark_task()
        self.creat_user_task()
        self.create_train_task()
        session.commit()

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
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.init), status_name="init"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.queueing), status_name="queueing"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.processing), status_name="processing"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.unlabel), status_name="unlabel"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.labeling), status_name="labeling"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.labeled), status_name="labeled"),
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.reviewing), status_name="reviewing"),    # auditing
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.approved), status_name="approved"),     # audited
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.fail), status_name="fail"),         # failed
                Status(app_id=1, created_by=1, status_id=int(StatusEnum.success), status_name="success"),
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
        from app.model import MarkJobModel
        if len(MarkJobModel().get_all()) == 0:
            mark_jobs = [
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务1", doc_type_id=1, mark_job_id=1,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeled)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务2", doc_type_id=1, mark_job_id=2,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeled)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务3", doc_type_id=1, mark_job_id=3,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeling)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务4", doc_type_id=2, mark_job_id=4,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.reviewing)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务5", doc_type_id=3, mark_job_id=5,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.reviewing)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务6", doc_type_id=4, mark_job_id=6,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeling)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务7", doc_type_id=4, mark_job_id=7,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务8", doc_type_id=5, mark_job_id=8,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeling)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务9", doc_type_id=5, mark_job_id=9,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务10", doc_type_id=6, mark_job_id=10,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务11", doc_type_id=7, mark_job_id=11,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务12", doc_type_id=8, mark_job_id=12,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务13", doc_type_id=9, mark_job_id=13,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务14", doc_type_id=9, mark_job_id=14,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务15", doc_type_id=10, mark_job_id=15,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeled)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务16", doc_type_id=10, mark_job_id=16,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeling)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务17", doc_type_id=10, mark_job_id=17,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务18", doc_type_id=11, mark_job_id=18,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务19", doc_type_id=11, mark_job_id=19,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务20", doc_type_id=5, mark_job_id=20,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务21", doc_type_id=6, mark_job_id=21,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务22", doc_type_id=6, mark_job_id=22,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.reviewing)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务23", doc_type_id=5, mark_job_id=23,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.reviewing)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务24", doc_type_id=2, mark_job_id=24,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.labeling)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务25", doc_type_id=2, mark_job_id=25,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务26", doc_type_id=2, mark_job_id=26,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.reviewing)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务27", doc_type_id=5, mark_job_id=27,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务28", doc_type_id=8, mark_job_id=28,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
                MarkJob(app_id=1, created_by=1, mark_job_name="标注任务29", doc_type_id=7, mark_job_id=29,
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.approved)),
            ]
            MarkJobModel().bulk_create(mark_jobs)
            session.commit()

    @staticmethod
    def create_train_job():
        from app.entity import TrainJob
        from app.model import TrainJobModel
        if len(TrainJobModel().get_all()) == 0:
            train_jobs = [
                TrainJob(app_id=1, created_by=1, train_job_name="模型1", doc_type_id=1,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型2", doc_type_id=1,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型3", doc_type_id=1,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型4", doc_type_id=2,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型5", doc_type_id=3,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型6", doc_type_id=4,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型7", doc_type_id=4,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型8", doc_type_id=5,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型9", doc_type_id=5,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型10", doc_type_id=6,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型11", doc_type_id=7,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型12", doc_type_id=8,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型13", doc_type_id=9,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型14", doc_type_id=9,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型15", doc_type_id=10,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型16", doc_type_id=10,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型17", doc_type_id=10,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型18", doc_type_id=11,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型19", doc_type_id=11,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型20", doc_type_id=5,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型21", doc_type_id=6,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型22", doc_type_id=6,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型23", doc_type_id=5,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型24", doc_type_id=2,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型25", doc_type_id=2,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型26", doc_type_id=2,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型27", doc_type_id=5,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型28", doc_type_id=8,
                         train_job_status=int(StatusEnum.success)),
                TrainJob(app_id=1, created_by=1, train_job_name="模型29", doc_type_id=7,
                         train_job_status=int(StatusEnum.success)),

            ]
            TrainJobModel().bulk_create(train_jobs)
            session.commit()

    @staticmethod
    def create_doc():
        from app.entity import Doc
        from app.model import DocModel
        from uuid import uuid4
        if DocModel().is_empty_table():
            docs = [
                Doc(app_id=1, created_by=1, doc_id=1, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                Doc(app_id=1, created_by=1, doc_id=2, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                Doc(app_id=1, created_by=1, doc_id=3, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                Doc(app_id=1, created_by=1, doc_id=4, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                Doc(app_id=1, created_by=1, doc_id=5, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
            ]
            DocModel().bulk_create(docs)
            session.commit()

    @staticmethod
    def create_mark_task():
        from app.entity import MarkTask
        from app.model import MarkTaskModel
        if MarkTaskModel().is_empty_table():
            mark_tasks = [
                MarkTask(app_id=1, created_by=1, mark_job_id=1, mark_task_id=1, doc_id=1, mark_task_status=int(StatusEnum.labeled)),
                MarkTask(app_id=1, created_by=1, mark_job_id=1, mark_task_id=2, doc_id=2, mark_task_status=int(StatusEnum.labeled)),
                MarkTask(app_id=1, created_by=1, mark_job_id=1, mark_task_id=3, doc_id=3, mark_task_status=int(StatusEnum.labeled)),
                MarkTask(app_id=1, created_by=1, mark_job_id=1, mark_task_id=4, doc_id=4, mark_task_status=int(StatusEnum.labeled)),
                MarkTask(app_id=1, created_by=1, mark_job_id=1, mark_task_id=5, doc_id=5, mark_task_status=int(StatusEnum.labeled)),
            ]
            MarkTaskModel().bulk_create(mark_tasks)
            session.commit()

    @staticmethod
    def creat_user_task():
        from app.entity import UserTask
        from app.model import UserTaskModel
        if UserTaskModel().is_empty_table():
            user_tasks = [
                UserTask(app_id=1, created_by=1, mark_task_id=1, annotator_id=3, user_task_status=int(StatusEnum.labeled)),
                UserTask(app_id=1, created_by=1, mark_task_id=2, annotator_id=3,
                         user_task_status=int(StatusEnum.labeled)),
                UserTask(app_id=1, created_by=1, mark_task_id=3, annotator_id=3,
                         user_task_status=int(StatusEnum.labeled)),
                UserTask(app_id=1, created_by=1, mark_task_id=4, annotator_id=3,
                         user_task_status=int(StatusEnum.labeled)),
                UserTask(app_id=1, created_by=1, mark_task_id=5, annotator_id=3,
                         user_task_status=int(StatusEnum.labeled)),

            ]
            UserTaskModel().bulk_create(user_tasks)
            session.commit()

    @staticmethod
    def create_train_task():
        from app.model import TrainTaskModel
        if TrainTaskModel().is_empty_table():
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=1, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=1)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=2, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=1)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=3, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=2)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=4, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=3)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=5, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=3)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=6, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=4)
            TrainTaskModel().create(app_id=1, created_by=1, train_task_id=7, train_model_name="test",
                                    train_status=int(StatusEnum.training), train_job_id=5)
        session.commit()