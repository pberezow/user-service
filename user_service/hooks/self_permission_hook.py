import falcon
from falcon import Request, Response


class IsSelfPermissionHook:
    def __init__(self, param_name: str = 'username'):
        self._param_name = param_name

    def __call__(self, req: Request, resp: Response, resource, params):
        if req.context.get('user', None) and not req.context.user.username == params[self._param_name]:
            raise falcon.HTTPUnauthorized()
        req.context.is_self = True
