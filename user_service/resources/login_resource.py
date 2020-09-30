import falcon
from falcon import Request, Response

from user_service.services import AuthService, JWTService
from user_service.mappers import UserMapper
from user_service.utils import BaseResource


class LoginResource(BaseResource):
    """
    Provides login resource.

    on_post - sets jwt token in `token` cookie.
        expects `username` and `password` in request body.
    """
    mapper = UserMapper(included_attributes={'username', 'password'})

    def __init__(self, auth_service: AuthService, jwt_service: JWTService):
        self._auth_service = auth_service
        self._jwt_service = jwt_service
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        data = req.media

        user_to = self.map_with_error(data)

        user = self._auth_service.authenticate_user(user_to.username, user_to.password)
        if not user:
            raise falcon.HTTPUnauthorized()

        token = self._jwt_service.create_jwt(user)
        refresh_token = self._jwt_service.create_refresh_token(token)

        resp.set_cookie('token', token)
        resp.set_cookie('refresh_token', refresh_token)
