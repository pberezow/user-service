import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.services import JWTService, AuthService


class RefreshTokenResource(BaseResource):
    """
    Provides resource for jwt session refresh.

    on_post - gets refresh token, validates it and returns new JWT with new refresh_token
    """
    def __init__(self, jwt_service: JWTService, auth_service: AuthService):
        self._jwt_service = jwt_service
        self._auth_service = auth_service
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        """
        Refresh JWT and creates new refresh_token.
        """
        refresh_token = req.media.get('refresh_token', None)
        if refresh_token is None:
            raise falcon.HTTPBadRequest(f'Refresh token is missing.')

        user_to = self._jwt_service.validate_refresh_token(refresh_token)
        if user_to is None:
            raise falcon.HTTPBadRequest('Invalid refresh token.')

        user_to = self._auth_service.refresh_user_data(user_to.username)
        if user_to is None or not user_to.is_active:
            raise falcon.HTTPUnauthorized()

        token = self._jwt_service.create_jwt(user_to)
        refresh_token = self._jwt_service.create_refresh_token(token)

        resp.set_cookie('token', token)
        resp.set_cookie('refresh_token', refresh_token)
