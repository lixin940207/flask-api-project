from app.common.log import logger
from app.common.extension import session
from app.common.common import NlpTaskEnum, StatusEnum


class Seeds:
    def create_seeds(self, debug=False):
        # Create seeds data from base tables
        self.create_nlp_task()
        self.create_status()
        if debug:
            self.create_doc_type()
            self.create_doc_term()
            self.create_mark_job()
            self.create_train_job()
            self.create_doc()
            self.create_mark_task()
            self.creat_user_task()
            self.create_train_task()
            self.create_evaluate_task()
        session.commit()

    @staticmethod
    def create_nlp_task():
        from app.entity import NlpTask
        from app.model import NlpTaskModel
        if len(NlpTaskModel().get_all()) == 0:
            init_nlp_tasks = []
            for i in NlpTaskEnum:
                init_nlp_tasks.append(NlpTask(app_id=1, created_by=1, nlp_task_id=int(i), nlp_task_name=i.name))
            NlpTaskModel().bulk_create(init_nlp_tasks)
            session.commit()
            logger.info(" [x] Seeds nlp_task has been created. ")

    @staticmethod
    def create_status():
        from app.entity import Status
        from app.model import StatusModel
        if len(StatusModel().get_all()) == 0:
            init_status = []
            for i in StatusEnum:
                init_status.append(Status(app_id=1, created_by=1, status_id=int(i), status_name=i.name))
            StatusModel().bulk_create(init_status)
            session.commit()
            logger.info(" [x] Seeds status has been created. ")

    @staticmethod
    def create_doc_type():
        from app.model import DocTypeModel
        if len(DocTypeModel().get_all()) == 0:
            doc_types = [
                dict(app_id=1, created_by=1, doc_type_id=1, doc_type_name="测试抽取项目1",
                        nlp_task_id=int(NlpTaskEnum.extract)),
                dict(app_id=1, created_by=1, doc_type_id=2, doc_type_name="测试抽取项目2",
                        nlp_task_id=int(NlpTaskEnum.extract)),
                dict(app_id=1, created_by=1, doc_type_id=3, doc_type_name="测试抽取项目3",
                        nlp_task_id=int(NlpTaskEnum.extract)),
                dict(app_id=1, created_by=1, doc_type_id=4, doc_type_name="测试抽取项目4",
                        nlp_task_id=int(NlpTaskEnum.extract)),
                dict(app_id=1, created_by=1, doc_type_id=5, doc_type_name="测试分类项目1",
                        nlp_task_id=int(NlpTaskEnum.classify)),
                dict(app_id=1, created_by=1, doc_type_id=6, doc_type_name="测试分类项目2",
                        nlp_task_id=int(NlpTaskEnum.classify)),
                dict(app_id=1, created_by=1, doc_type_id=7, doc_type_name="测试分类项目3",
                        nlp_task_id=int(NlpTaskEnum.classify)),
                dict(app_id=1, created_by=1, doc_type_id=8, doc_type_name="测试关系项目1",
                        nlp_task_id=int(NlpTaskEnum.relation)),
                dict(app_id=1, created_by=1, doc_type_id=9, doc_type_name="测试关系项目2",
                        nlp_task_id=int(NlpTaskEnum.relation)),
                dict(app_id=1, created_by=1, doc_type_id=10, doc_type_name="测试分词项目1",
                        nlp_task_id=int(NlpTaskEnum.wordseg)),
                dict(app_id=1, created_by=1, doc_type_id=11, doc_type_name="测试分词项目2",
                        nlp_task_id=int(NlpTaskEnum.wordseg)),
            ]
            DocTypeModel().bulk_create(doc_types)
            session.commit()

    @staticmethod
    def create_doc_term():
        from app.model import DocTermModel
        if len(DocTermModel().get_all()) == 0:
            DocTermModel().create(app_id=1, created_by=1, doc_term_id=1, doc_term_name="人名", doc_term_alias="nr",
                                  doc_type_id=1)
            DocTermModel().create(app_id=1, created_by=1, doc_term_id=2, doc_term_name="地名", doc_term_alias="ns",
                                  doc_type_id=1)
            DocTermModel().create(app_id=1, created_by=1, doc_term_id=3, doc_term_name="机构名", doc_term_alias="nt",
                                  doc_type_id=1)
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
                        mark_job_type="e_doc", mark_job_status=int(StatusEnum.success)),
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
        from app.model import DocModel
        from uuid import uuid4
        if DocModel().is_empty_table():
            docs = [
                dict(app_id=1, created_by=1, doc_id=1, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                dict(app_id=1, created_by=1, doc_id=2, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                dict(app_id=1, created_by=1, doc_id=3, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                dict(app_id=1, created_by=1, doc_id=4, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
                dict(app_id=1, created_by=1, doc_id=5, doc_raw_name="doc1.pdf", doc_unique_name=str(uuid4())),
            ]
            DocModel().bulk_create(docs)
            session.commit()

    @staticmethod
    def create_mark_task():
        from app.model import MarkTaskModel
        if MarkTaskModel().is_empty_table():
            mark_tasks = [
                dict(app_id=1, created_by=1, mark_job_id=1, mark_task_id=1, doc_id=1,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=1, mark_task_id=2, doc_id=2,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=1, mark_task_id=3, doc_id=3,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=1, mark_task_id=4, doc_id=4,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=1, mark_task_id=5, doc_id=5,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=8, mark_task_id=6, doc_id=1,
                     mark_task_status=int(StatusEnum.approved)),
                dict(app_id=1, created_by=1, mark_job_id=8, mark_task_id=7, doc_id=2,
                     mark_task_status=int(StatusEnum.approved)),
                dict(app_id=1, created_by=1, mark_job_id=9, mark_task_id=8, doc_id=3,
                     mark_task_status=int(StatusEnum.approved)),
                dict(app_id=1, created_by=1, mark_job_id=9, mark_task_id=9, doc_id=4,
                     mark_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_job_id=9, mark_task_id=10, doc_id=5,
                     mark_task_status=int(StatusEnum.labeled)),
            ]
            MarkTaskModel().bulk_create(mark_tasks)
            session.commit()

    @staticmethod
    def creat_user_task():
        from app.model import UserTaskModel
        if UserTaskModel().is_empty_table():
            user_tasks = [
                dict(app_id=1, created_by=1, mark_task_id=1, annotator_id=3,
                     user_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_task_id=2, annotator_id=3,
                     user_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_task_id=3, annotator_id=3,
                     user_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_task_id=4, annotator_id=3,
                     user_task_status=int(StatusEnum.labeled)),
                dict(app_id=1, created_by=1, mark_task_id=5, annotator_id=3,
                     user_task_status=int(StatusEnum.labeled)),
            ]
            UserTaskModel().bulk_create(user_tasks)
            session.commit()

    @staticmethod
    def create_train_task():
        from app.model import TrainTaskModel
        if TrainTaskModel().is_empty_table():
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train1", train_status=int(StatusEnum.online), train_job_id=1)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train2", train_status=int(StatusEnum.success), train_job_id=2)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train3", train_status=int(StatusEnum.training), train_job_id=3)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train4", train_status=int(StatusEnum.training), train_job_id=4)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train5", train_status=int(StatusEnum.training), train_job_id=5)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train6", train_status=int(StatusEnum.training), train_job_id=6)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train7", train_status=int(StatusEnum.training), train_job_id=7)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train8", train_status=int(StatusEnum.online), train_job_id=8)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train9", train_status=int(StatusEnum.success), train_job_id=9)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train10", train_status=int(StatusEnum.training), train_job_id=10)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train11", train_status=int(StatusEnum.training), train_job_id=11)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train12", train_status=int(StatusEnum.training), train_job_id=12)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train13", train_status=int(StatusEnum.training), train_job_id=13)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train14", train_status=int(StatusEnum.training), train_job_id=14)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train15", train_status=int(StatusEnum.online), train_job_id=15)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train16",  train_status=int(StatusEnum.success), train_job_id=16)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train17", train_status=int(StatusEnum.training), train_job_id=17)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train18", train_status=int(StatusEnum.training), train_job_id=18)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train19", train_status=int(StatusEnum.training), train_job_id=19)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train20", train_status=int(StatusEnum.training), train_job_id=20)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train21", train_status=int(StatusEnum.training), train_job_id=21)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train22", train_status=int(StatusEnum.training), train_job_id=22)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train23", train_status=int(StatusEnum.online), train_job_id=23)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train24", train_status=int(StatusEnum.success), train_job_id=24)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train25", train_status=int(StatusEnum.training), train_job_id=25)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train26", train_status=int(StatusEnum.training), train_job_id=26)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train27", train_status=int(StatusEnum.training), train_job_id=27)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train28", train_status=int(StatusEnum.training), train_job_id=28)
            TrainTaskModel().create(app_id=1, created_by=1, train_model_name="train29", train_status=int(StatusEnum.training), train_job_id=29)
        session.commit()

    @staticmethod
    def create_evaluate_task():
        from app.model import EvaluateTaskModel
        if EvaluateTaskModel().is_empty_table():
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=1, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=1)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=2, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=1)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=3, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=2)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=4, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=3)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=5, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=3)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=6, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=4)
            EvaluateTaskModel().create(app_id=1, created_by=1, evaluate_task_id=7, evaluate_task_name="test",
                                       evaluate_task_status=int(StatusEnum.success), train_task_id=5)
        session.commit()
