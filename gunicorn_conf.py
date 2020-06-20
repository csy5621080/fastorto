bind = '0.0.0.0:8050'
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'

accesslog = "/var/log/gunicorn_access.log"  # 访问日志文件
errorlog = "/var/log/gunicorn_error.log"  # 错误日志文件