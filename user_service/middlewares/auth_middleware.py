import jwt
import os
import falcon
from falcon import Request, Response
from typing import Optional, Set
from user_service.services.user_crud_service import UserService


class AuthMiddleware:

    def __init__(self, user_service: UserService, allowed_paths: Optional[Set[str]] = None):
        self._user_service = user_service
        self._allowed_paths = allowed_paths or set()

    def process_request(self, req: Request, resp: Response):
        if req.path in self._allowed_paths:
            return

        token = req.get_header('Authorization')
        if token is None:
            # no token provided
            raise falcon.HTTPUnauthorized()

        user_to = self._user_service.get_user_from_jwt(token)
        if user_to is None:
            # invalid token
            raise falcon.HTTPUnauthorized()

        req.context.user = user_to
