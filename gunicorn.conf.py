import multiprocessing

bind = "0.0.0.0:5000"
workers = 1
threads = 4
worker_class = "gthread"
timeout = 120
max_requests = 1000
max_requests_jitter = 50