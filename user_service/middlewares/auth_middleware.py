import falcon
from falcon import Request, Response
from typing import Optional, Set

from user_service.services.jwt_service import JWTService


class AuthMiddleware:
    """
    Middleware for user's Authorization. Authorization is done through JWT passed in `Authorization` header.
        If authorization fails, then falcon.HTTPUnauthorized is raised, otherwise user transport object with
        provided payload is set in req.context.user.
    """
    def __init__(self, jwt_service: JWTService, allowed_paths: Optional[Set[str]] = None):
        self._jwt_service = jwt_service
        self._allowed_paths = allowed_paths or set()

    def process_request(self, req: Request, resp: Response):
        if req.path in self._allowed_paths:
            return

        token_header = req.get_header('Authorization')
        if token_header is None or not token_header.startswith('Bearer '):
            # no token provided
            raise falcon.HTTPUnauthorized()

        token = token_header[7:]
        user_to = self._jwt_service.get_user_from_jwt(token)
        if user_to is None:
            # invalid token
            raise falcon.HTTPUnauthorized()

        req.context.user = user_to
