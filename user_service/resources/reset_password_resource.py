import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.services import ResetTokenService
from user_service.utils.validators import password_validator as is_valid_password


class ResetPasswordResource(BaseResource):
    """
    on post - creates new token
    """

    def __init__(self, reset_token_service: ResetTokenService):
        self._reset_token_service = reset_token_service
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        data = req.media or {}
        token = data.get('token', None)
        password = data.get('password', None)

        if token is None or password is None:
            # missing payload
            raise falcon.HTTPBadRequest()

        if not is_valid_password(password):
            # invalid password
            raise falcon.HTTPBadRequest()

        # Set new password
        success = self._reset_token_service.reset_password(token, password)
        if not success:
            # wrong token
            raise falcon.HTTPBadRequest()

        resp.status = falcon.HTTP_200
