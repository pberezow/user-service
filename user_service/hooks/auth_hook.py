import falcon
from falcon import Request, Response
from user_service.services import JWTService


class AuthHook:
    """
    Hook for user's Authorization. Authorization is done through JWT passed in `Authorization` header.
        If authorization fails, then falcon.HTTPUnauthorized is raised.
    """
    def __init__(self, jwt_service: JWTService):
        self._jwt_service = jwt_service

    def __call__(self, req: Request, resp: Response):
        token = req.get_header('Authorization')
        if token is None:
            # no token provided
            raise falcon.HTTPUnauthorized()

        user_to = self._jwt_service.get_user_from_jwt(token)
        if user_to is None:
            # invalid token
            raise falcon.HTTPUnauthorized()

        req.context.user = user_to
