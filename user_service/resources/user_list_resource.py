import falcon
from falcon import Request, Response
from datetime import datetime

from user_service.utils import BaseResource
from user_service.mappers import UserMapper
from user_service.services import UserCRUDService
from user_service.hooks import IsAdminPermissionHook


class UserListResource(BaseResource):
    """
    Provides user resource for operations on multiple users and creating user.

    on_get - returns list of users with same licence_id
    on post - creates new user
    """
    mapper = UserMapper(included_attributes={'licence_id', 'username', 'password', 'is_admin', 'first_name',
                                             'last_name', 'email', 'phone_number', 'address', 'position', 'is_active',
                                             'date_joined', 'last_login'})

    def __init__(self, user_crud_service: UserCRUDService):
        self._user_crud_service = user_crud_service
        super().__init__()

    def on_get(self, req: Request, resp: Response):
        user = req.context.user

        users_to = self._user_crud_service.get_users_for_licence(user.licence_id)
        resp.status = falcon.HTTP_200
        resp.media = [u.as_json() for u in users_to]

    @falcon.before(IsAdminPermissionHook())
    def on_post(self, req: Request, resp: Response):
        user = req.context.user

        data = req.media or {}
        data['licence_id'] = user.licence_id
        data['is_active'] = True
        data['last_login'] = None
        data['date_joined'] = datetime.now()
        data['is_admin'] = data.get('is_admin', False)
        data['first_name'] = data.get('first_name', '')
        data['last_name'] = data.get('last_name', '')
        data['phone_number'] = data.get('phone_number', '')
        data['address'] = data.get('address', '')
        data['position'] = data.get('position', '')

        user_to = self.map_with_error(data)
        # TODO - catch exceptions
        user_to = self._user_crud_service.create_user(user_to)
        if user_to is None:
            raise falcon.HTTPBadRequest()

        resp.status = falcon.HTTP_CREATED
        resp.media = user_to.as_json()
