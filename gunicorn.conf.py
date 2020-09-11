import multiprocessing


bind = '0.0.0.0:8000'
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = 'gthread'  # 'eventlet'  # gthread for threads - and set threads var
# threads = multiprocessing.cpu_count() * 2 + 1
threads = 1
proc_name = 'user_service'
max_requests = 0  # num of request after which worker will restart (prevent memory leaks)
