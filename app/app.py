import typing
from flask import Flask, logging
from app.config.config import Configs
from app.common.log import add_console_handler, add_file_handler
from app.common.extension import register_extension
from app.common.handler import register_handler
from app.resource import register_blueprint
from app.common.middleware import register_middleware
from app.resource.v2.common_api import register_common_api
from app.common.seeds import Seeds


def create_app(env: str = 'development', override_config: typing.Dict = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Configs[env])
    if override_config and isinstance(override_config, dict):
        app.config.update(override_config)

    app.logger.removeHandler(logging.default_handler)
    add_console_handler(app.logger)
    add_file_handler(app.logger)

    register_extension(app)
    register_handler(app)
    register_middleware(app)
    register_blueprint(app)
    register_common_api(app)

    with app.app_context():
        try:
            Seeds().create_seeds(debug=False)
            # pass
        except Exception as e:
            app.logger.warning(" [-] Create seeds failed, may caused by first time start up. ")
            app.logger.warning(e)

    return app
