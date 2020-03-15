from app.common.log import logger
from app.common.extension import session


def create_seeds():
    # Create seeds data from base tables
    create_nlp_task()
    create_status()


def create_nlp_task():
    from app.entity import NlpTask
    from app.model import NlpTaskModel
    if len(NlpTaskModel().get_all()) == 0:
        init_nlp_tasks = [
            NlpTask(app_id=1, created_by=1, nlp_task_name="extract"),
            NlpTask(app_id=1, created_by=1, nlp_task_name="classify"),
            NlpTask(app_id=1, created_by=1, nlp_task_name="wordseg"),
            NlpTask(app_id=1, created_by=1, nlp_task_name="relation"),
        ]
        NlpTaskModel().bulk_create(init_nlp_tasks)
        session.commit()
        logger.info(" [x] Seeds nlp_task has been created. ")


def create_status():
    from app.entity import Status
    from app.model import StatusModel
    if len(StatusModel().get_all()) == 0:
        init_status = [
            Status(app_id=1, created_by=1, status_name="init"),
            Status(app_id=1, created_by=1, status_name="queueing"),
            Status(app_id=1, created_by=1, status_name="processing"),
            Status(app_id=1, created_by=1, status_name="unlabel"),
            Status(app_id=1, created_by=1, status_name="labeled"),
            Status(app_id=1, created_by=1, status_name="reviewing"),    # auditing
            Status(app_id=1, created_by=1, status_name="approved"),     # audited
            Status(app_id=1, created_by=1, status_name="fail"),         # failed
            Status(app_id=1, created_by=1, status_name="success"),
        ]
        StatusModel().bulk_create(init_status)
        session.commit()
        logger.info(" [x] Seeds status has been created. ")


