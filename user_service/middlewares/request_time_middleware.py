from falcon import Request, Response
from time import time


class RequestTimeMiddleware:
    """
    Middleware which measures response time of service. Used for benchmarking.
    """
    def __init__(self):
        pass

    def process_request(self, req: Request, resp: Response):
        start_time = time()
        req.context.start_time = start_time

    def process_response(self, req: Request, resp: Response, resource, req_succeeded):
        end_time = time()
        print(f'Response time: {end_time - req.context.start_time} sec.')
