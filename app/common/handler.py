import typing
from flask import Flask, jsonify, Response
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from .log import log_err


def register_handler(app: Flask) -> None:
    @app.errorhandler(404)
    @log_err
    def not_found(err: HTTPException) -> typing.Tuple[Response, typing.Optional[int]]:
        return jsonify({
            'message': "Not Found"
        }), err.code

    @app.errorhandler(400)
    @log_err
    def bad_request(err: HTTPException) -> typing.Tuple[Response, typing.Optional[int]]:
        return jsonify({
            'message': "Bad Request"
        }), err.code

    @app.errorhandler(ValidationError)
    @log_err
    def validation_error(err: ValidationError) -> typing.Tuple[Response, typing.Optional[int]]:
        return jsonify(err.messages), 400

    @app.errorhandler(NoResultFound)
    @log_err
    def no_result_found(err: NoResultFound) -> typing.Tuple[Response, typing.Optional[int]]:
        return jsonify({
            'message': str(err)
        }), 400

    @app.errorhandler(Exception)
    @log_err
    def err_not_catch(err: Exception) -> typing.Tuple[Response, typing.Optional[int]]:
        return jsonify({
            "message": "服务器内部错误或网络错误。",
            "exception": str(err)
        }), 500
