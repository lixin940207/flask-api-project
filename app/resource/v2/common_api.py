from flask import Flask, send_from_directory
from flask_restful import Api, Resource, abort


class FileResource(Resource):
    def get(self: Resource, path: str):
        if not path.split('/', 1)[0] in ['upload', 'tmp', 'docs']:
            abort(404)
        return send_from_directory('..', path)


def register_common_api(app: Flask):
    common_api = Api(app, prefix='', decorators=[])
    common_api.add_resource(FileResource, '/file/<path:path>')
