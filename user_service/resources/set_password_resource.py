import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.mappers import UserMapper
from user_service.services import UserCRUDService, AuthService
from user_service.hooks import IsSelfPermissionHook


class SetPasswordResource(BaseResource):
    mapper = UserMapper(included_attributes={'password'})

    def __init__(self, user_crud_service: UserCRUDService, auth_service: AuthService):
        self._user_crud_service = user_crud_service
        self._auth_service = auth_service
        super().__init__()

    @falcon.before(IsSelfPermissionHook(param_name='username'))
    def on_put(self, req: Request, resp: Response, username: str):
        data = req.media

        old_password = data.get('old_password', None)
        if old_password is None:
            raise falcon.HTTPBadRequest()

        # validate new password
        user_to = self.map_with_error(data)

        # validate user's current password
        user = self._auth_service.authenticate_user(username, old_password)
        if user is None:
            raise falcon.HTTPBadRequest()

        success = self._user_crud_service.set_password(username, user_to.password)
        if not success:
            # todo - db error?
            raise falcon.HTTPBadRequest()
