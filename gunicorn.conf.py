import os

timeout = 120
bind = f"{os.environ['APP_HOST']}:{os.environ['APP_PORT']}"
workers = os.environ["WORKER_COUNT"]
accesslog = "-"
access_log_format = "%(t)s %(h)s - %(r)s %(s)s %(f)s %(a)s"
