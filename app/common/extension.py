from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler

# apscheduler = APScheduler()
db = SQLAlchemy()
session = db.session
ma = Marshmallow()
cors = CORS(resources=r'/*', supports_credentials=True)
limiter = Limiter(key_func=get_remote_address, default_limits=['120/minute'])


def register_extension(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    ma.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    # apscheduler.init_app(app)
    # apscheduler.start()
