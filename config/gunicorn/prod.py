import multiprocessing

wsgi_app = "bookshop.wsgi:application"
workers = multiprocessing.cpu_count() * 2 + 1
bind = "127.0.0.1:8000"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = True
pidfile = "/var/run/gunicorn/prod.pid"
daemon = True
keyfile = "/opt/apps/ssdb/cert/localhost.key"
certfile = "/opt/apps/ssdb/cert/localhost.crt"
