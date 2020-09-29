from falcon import Request, Response
from typing import Optional


class CrossOriginMiddleware:
    """
    Middleware for CORS.
    """
    origin = '*'  # DEFAULT_ACCESS_CONTROL_ALLOW_ORIGIN
    headers = '*'  # DEFAULT_ACCESS_CONTROL_ALLOW_HEADERS
    credentials = 'true'  # DEFAULT_ACCESS_CONTROL_ALLOW_CREDENTIALS
    max_age = '1728000'  # DEFAULT_ACCESS_CONTROL_MAX_AGE

    def __init__(self, origin: Optional[str] = None, headers: Optional[str] = None, credentials: Optional[str] = None,
                 max_age: Optional[str] = None):
        if origin is not None:
            self.origin = origin
        if headers is not None:
            self.headers = headers
        if credentials is not None:
            self.credentials = credentials
        if max_age is not None:
            self.max_age = max_age

    def process_request(self, req: Request, resp: Response):
        pass

    def process_response(self, req: Request, resp: Response, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', req.headers.get('Origin', self.origin))
        resp.set_header('Access-Control-Allow-Credentials', self.credentials)
        if req.method == 'OPTIONS':
            resp.set_header('Access-Control-Allow-Headers', self.headers)
            resp.set_header('Access-Control-Max-Age', self.max_age)  # for OPTIONS caching
