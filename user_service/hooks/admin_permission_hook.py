import falcon
from falcon import Request, Response


class IsAdminPermissionHook:
    """
    Hook used to validate if user has admin permission (checks is_admin claim in JWT).
        raises falcon.HTTPForbidden exception if user doesn't have admin permissions.
    """
    def __init__(self):
        pass

    def __call__(self, req: Request, resp: Response, resource, params):
        if req.context.get('user', None) and not req.context.user.is_admin:
            req.context.is_admin = False
            raise falcon.HTTPForbidden()
        req.context.is_admin = True
