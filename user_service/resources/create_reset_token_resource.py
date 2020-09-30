import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.services import ResetTokenService
from user_service.utils.validators import email_validator as is_valid_email


class CreateResetTokenResource(BaseResource):
    """
    on post - creates new token
    """

    def __init__(self, reset_token_service: ResetTokenService):
        self._reset_token_service = reset_token_service
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        data = req.media or {}
        email = data.get('email', None)
        if email is None and not is_valid_email(email):
            raise falcon.HTTPBadRequest()

        # run task on new thread
        self._reset_token_service.create_token_and_send_email(email)

        resp.status = falcon.HTTP_200
