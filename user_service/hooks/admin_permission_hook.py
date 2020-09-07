import falcon
from falcon import Request, Response


class IsAdminPermissionHook:
    def __init__(self):
        pass

    def __call__(self, req: Request, resp: Response, resource, params):
        if req.context.get('user', None) and not req.context.user.is_admin:
            raise falcon.HTTPUnauthorized()
        req.context.is_admin = True
