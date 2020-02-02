import multiprocessing


bind = '0.0.0.0:3000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'eventlet'  # gthread for threads - and set threads var
proc_name = 'user_service'
max_requests = 0  # num of request after which worker will restart (prevent memory leaks)