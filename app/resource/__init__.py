from flask import Flask


def register_blueprint(flask_app: Flask) -> None:
    from . import v2
    flask_app.register_blueprint(v2.blueprint)
