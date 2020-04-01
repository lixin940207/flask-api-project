from contextlib import contextmanager
from flask import current_app
import time
import redis
from app.config.config import RedisConfigMixin

host = RedisConfigMixin.REDIS_HOST
port = RedisConfigMixin.REDIS_PORT
db = RedisConfigMixin.REDIS_DATABASE
pool = redis.ConnectionPool(host=host, port=port)
r = redis.Redis(connection_pool=pool, db=db)  # type: ignore


@contextmanager
def lock(key):
    key = f'lock_{key}'
    while r.get(key):
        time.sleep(3)
    r.set(key, 'True')
    try:
        yield
    except Exception as e:
        current_app.logger.error(e)
        raise
    finally:
        r.delete(key)
