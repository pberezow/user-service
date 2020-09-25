import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.services import ResetTokenService


class ValidateResetTokenResource(BaseResource):
    """
    on post - validated token
    """

    def __init__(self, reset_token_service: ResetTokenService):
        self._reset_token_service = reset_token_service
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        data = req.media or {}
        token = data.get('token', None)
        if token is None:
            raise falcon.HTTPBadRequest()

        # run validation
        if not self._reset_token_service.validate_token(token) or self._reset_token_service.get_user_id(token) is None:
            resp.media = {
                'is_valid': False
            }
        else:
            resp.media = {
                'is_valid': True
            }

        resp.status = falcon.HTTP_200
