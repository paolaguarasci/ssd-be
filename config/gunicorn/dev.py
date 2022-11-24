wsgi_app = "dressy.wsgi:application"
loglevel = "debug"
workers = 2
bind = "0.0.0.0:8000"
reload = True
accesslog = errorlog = "dev.log"
capture_output = True
pidfile = "dev.pid"
daemon = True
keyfile = "cert/localhost.key"
certfile = "cert/localhost.crt"
