import json
import base64
from flask import Flask, Response, request, g
from app.common.log import bind_request_id_to_g, logger
from app.common.log import get_request_id


def register_middleware(app: Flask) -> None:
    @app.before_first_request
    def before_first_request() -> None:
        pass

    @app.before_request
    def before_request() -> None:
        s = base64.b64decode(request.headers.get('User-Info', '')).decode('utf-8')
        if s:
            user_info = json.loads(s)
        else:
            user_info = {}
        g.app_id = request.args.get('app_id') or user_info.get('app_id', 0)
        g.user_id = request.args.get('user_id') or user_info.get('id', 0)
        g.user_name = request.args.get('username') or user_info.get('username', '')
        g.user_roles = request.args.getlist('user_roles') or [r.get('name') for r in user_info.get('roles', [])]
        try:
            g.user_groups = request.args.getlist('groups') or [r.get('id') for r in user_info.get('groups', [1])]
        except:
            g.user_groups = [-1]
        logger.info({
            "app_id": g.app_id,
            "user_id": g.user_id,
            "user_name": g.user_name,
            "user_roles": g.user_roles,
        })
        bind_request_id_to_g()

    @app.after_request
    def after_request(resp: Response) -> Response:
        if isinstance(resp.get_json(), dict):
            # use replace not json.load/dumps for speed
            resp.data = resp.data.replace(b'{', bytes('{\n"request_id":"%s",' % get_request_id(), 'utf-8'), 1)
        return resp
