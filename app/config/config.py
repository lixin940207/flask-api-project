import os
from pathlib import Path
from flask import Config, current_app

BASE_PATH: str = os.getcwd()
ROOT_PATH: Path = Path(__file__).parents[1]  # is same as 'BASE_PATH', but more conveniently to be used


def get_config_from_app(*args, **kwargs):
    return current_app.config.get(*args, **kwargs)


class BasicConfig(Config):
    SECRET_KEY = 'datagrand-nlp-platform-api'


class OCRServiceConfigMixin:
    COMMON_OCR_URL = os.getenv('COMMON_OCR_URL', 'http://10.120.13.223:51000')
    # COMMON_OCR_URL = os.getenv('COMMON_OCR_URL', 'http://172.16.0.26:51000')
    OCR_LICENSE_URL = os.getenv('OCR_LICENSE_URL', 'http://10.120.13.223:51001')
    OCR_IDCARD_URL = os.getenv('OCR_IDCARD_URL', 'http://10.120.13.223:51001')  # 待提供
    OCR_INVOICE_URL = os.getenv('OCR_INVOICE_URL', 'http://10.120.13.223:51001')  # 待提供

    # COMMON_OCR_URL = os.getenv('COMMON_OCR_URL', 'http://localhost:51000')
    # OCR_LICENSE_URL = os.getenv('OCR_LICENSE_URL', 'http://localhost:51001')


class PdfActionConfigMixin:
    PDF_PRINTER = os.getenv('PDF_PRINTER_URL', 'http://pdf_printer:10022/api/marker')


class SqlalchemyConfigMixin:
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:53306/szse"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(
        os.getenv('MYSQL_USER', 'root'),
        os.getenv('MYSQL_PASSWORD', 'root'),
        os.getenv('MYSQL_HOST', '127.0.0.1'),
        os.getenv('MYSQL_PORT', 43306),
        os.getenv('MYSQL_DATABASE', 'nlp_platform'),
        os.getenv('MYSQL_CHARSET', 'utf8mb4')
    )
    # 调试SQL语句时使用，慎开
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 280


# Redis实例的生成不应该依赖于Flask实例，所以生成redis的实例直接引用的此配置
class RedisConfigMixin:
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DATABASE = os.getenv('REDIS_DATABASE', 0)


class AsyncQueueConfigMixin:
    EXTRACT_TRAIN_QUEUE_KEY = 'queue:a'
    EXTRACT_TASK_QUEUE_KEY = 'task:contract:queue'
    EXTRACT_EVALUATE_QUEUE_KEY = 'model:evaluate:queue'
    RELATION_TRAIN_QUEUE_KEY = 'queue:a'
    RELATION_TASK_QUEUE_KEY = 'task:contract:queue'
    RELATION_EVALUATE_QUEUE_KEY = 'model:evaluate:queue'
    WORDSEG_TRAIN_QUEUE_KEY = 'queue:a'
    WORDSEG_TASK_QUEUE_KEY = 'task:contract:queue'
    WORDSEG_EVALUATE_QUEUE_KEY = 'model:evaluate:queue'
    CLASSIFY_MODEL_QUEUE_KEY = 'queue:classify:a'
    # 新词发现队列
    NEW_WORD_TASK_QUEUE_KEY = 'task:newword_queue'
    TEXT_CLUSTERING_TASK_QUEUE_KEY = 'task:clustering:queue'
    # 字词向量队列
    WORD_EMBEDDING_TASK_QUEUE = 'task:embedding:queue'
    # 训练数据导出队列
    DATA_EXPORT_QUEUE_KEY = 'queue:data_export:a'


class NlpServiceConfigMixin:
    CLASSIFY_MODEL_ONLINE = os.getenv('CLASSIFY_MODEL_ONLINE', 'http://model_manager_classify:8000/reload')
    TEXT_CLASSIFY_SERVER_URL = 'http://{}:{}/classify'.format(
        os.getenv('TEXT_CLASSIFY_SERVER_HOST', 'model_manager_classify'),
        os.getenv('TEXT_CLASSIFY_SERVER_PORT', 8000)
    )

    EXTRACT_MODEL_ONLINE = os.getenv('EXTRACT_MODEL_ONLINE', 'http://model_manager:8000/model_reload')

    TIMES_WORDSEG_ONLINE = os.getenv('TIMES_WORDSEG_ONLINE', 'http://segmentation:5001/segment')
    # 文本摘要功能模块接口
    TEXT_SUMMARY_ONLINE = os.getenv('TEXT_SUMMARY_ONLINE', 'http://text_summary:11000/textsummary/txt')
    # 依存句法分析功能模块接口
    DEPENDENCY_PARSER_ONLINE = os.getenv('DEPENDENCY_PARSER_ONLINE', 'http://dependency_parser:59989/parser/test')
    # 命名实体识别（抽取）在线接口
    ENTIR_EXTRACT_ONLINE = os.getenv('ENTIR_EXTRACT_ONLINE', 'http://assemble_dp_subservice:8000/extract')

    EXPORT_LABEL_ONLINE = os.getenv('EXPORT_LABEL_ONLINE', 'http://offline_nlp:8000/gen_training_data')


class DevelopmentConfig(
    BasicConfig,
    OCRServiceConfigMixin,
    PdfActionConfigMixin,
    SqlalchemyConfigMixin,
    RedisConfigMixin,
    AsyncQueueConfigMixin,
    NlpServiceConfigMixin,
):
    ENV = "development"
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
    AUTHMGR_FORWARD_INIT_URL = 'http://{}:{}/forward/forward_init/'.format(
        os.getenv('AUTHMGR_HOST', 'authmgr'),
        os.getenv('AUTHMGR_PORT', 10001)
    )


class TestingConfig(BasicConfig):
    ENV = "testing"
    DEBUG = False
    TESTING = True
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(BasicConfig):
    # TODO 正确配置生产环境配置
    ENV = "production"
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


Configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
