import os

bind = "0.0.0.0:10001"
workers = 9
backlog = 512
timeout = 10 * 60
worker_class = 'gevent'
threads = 4
loglevel = 'info'
access_log_format = '%(t)s - %(p)s - %(h)s - %(r)s - %(s)s - %(L)s - %(b)s - %(f)s - %(a)s'

if not os.path.exists('./logs'):
    os.makedirs('./logs')

accesslog = "./logs/access.log"
errorlog = "./logs/error.log"

max_requests = 1000
max_requests_jitter = 50
