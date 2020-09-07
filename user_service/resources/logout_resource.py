import falcon
import json
from falcon import Request, Response

from user_service.utils.base_resource import BaseResource


class LogoutResource(BaseResource):
    def __init__(self):
        super().__init__()

    def on_post(self, req: Request, resp: Response):
        resp.unset_cookie('token')
