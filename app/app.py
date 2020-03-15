import typing
from flask import Flask, logging
from app.config.config import Configs
from app.common.log import add_console_handler, add_file_handler
from app.common.extension import register_extension
from app.common.handler import register_handler
from app.resource import register_blueprint
from app.common.middleware import register_middleware
from app.resource.v2.common_api import register_common_api
from app.common.seeds import create_seeds


def create_app(env: str = 'development', override_config: typing.Dict = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Configs[env])
    if override_config and isinstance(override_config, dict):
        app.config.update(override_config)

    app.logger.removeHandler(logging.default_handler)
    add_console_handler(app.logger)
    add_file_handler(app.logger)

    register_extension(app)
    app.logger.info(" [x] Extensions Registered.")
    register_handler(app)
    app.logger.info(" [x] Handlers Registered.")
    register_middleware(app)
    app.logger.info(" [x] Middleware Registered.")
    register_blueprint(app)
    app.logger.info(" [x] Blueprint Registered.")
    register_common_api(app)

    with app.app_context():
        create_seeds()

    app.logger.info(" [x] ----- Flask app started -----")
    return app
