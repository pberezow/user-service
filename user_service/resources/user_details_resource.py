import falcon
from falcon import Response, Request

from user_service.utils import BaseResource
from user_service.services import UserCRUDService
from user_service.mappers import UserMapper
from user_service.hooks import IsAdminPermissionHook, IsSelfPermissionHook, OrPermissionsHook


class UserDetailsResource(BaseResource):
    """
    Provides user resource with actions on specific user. (distinguished by username)

    on_get - returns details about user.
    on_put - changes user's data.
    on_delete - removes user (sets is_active = False)
    """
    mapper = UserMapper(included_attributes={'username', 'email', 'is_admin', 'first_name', 'last_name', 'phone_number',
                                             'address', 'position', })
    response_attributes = ['id', 'licence_id', 'username', 'email', 'is_admin', 'first_name', 'last_name',
                           'phone_number', 'address', 'position', 'last_login', 'date_joined', 'is_active', 'groups']

    def __init__(self, user_crud_service: UserCRUDService):
        self._user_crud_service = user_crud_service
        super().__init__()

    def on_get(self, req: Request, resp: Response, username: str):
        """Get user by username."""
        user = req.context.user

        user_to = self._user_crud_service.get_user(user.licence_id, username=username)
        if user_to is None:
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        if not user.is_admin and not user_to.is_active:
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        resp.status = falcon.HTTP_OK
        user = user_to.as_json()
        filtered_user = {key: user[key] for key in self.response_attributes}
        resp.media = filtered_user

    @falcon.before(OrPermissionsHook([IsSelfPermissionHook(param_name='username'), IsAdminPermissionHook()]))
    def on_put(self, req: Request, resp: Response, username: str):
        """Edit user data."""
        user = req.context.user

        data = req.media
        # validate data
        self.validate_with_error(data, partial=True, subset_of_attributes=set(data.keys()))

        user_to = self._user_crud_service.set_user_data(username, data)
        if not user_to:
            # does not exist or db constraints violated TODO
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        resp.status = falcon.HTTP_OK
        user = user_to.as_json()
        resp.media = {key: user[key] for key in self.response_attributes}

    @falcon.before(IsAdminPermissionHook())
    def on_delete(self, req: Request, resp: Response, username: str):
        """Delete user. (set is_active=False)"""
        user = req.context.user

        user_to = self._user_crud_service.remove_user(user.licence_id, username=username)
        if user_to is None:
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        resp.status = falcon.HTTP_200
