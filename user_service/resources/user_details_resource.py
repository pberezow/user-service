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

    def __init__(self, user_crud_service: UserCRUDService):
        self._user_crud_service = user_crud_service
        super().__init__()

    def on_get(self, req: Request, resp: Response, username: str):
        """Get user by username."""
        user = req.context.user

        user_to = self._user_crud_service.get_user(user.licence_id, username=username)
        if user_to is None:
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        resp.status = falcon.HTTP_200
        resp.media = user_to.as_json()

    @falcon.before(OrPermissionsHook([IsSelfPermissionHook(param_name='username'), IsAdminPermissionHook()]))
    def on_put(self, req: Request, resp: Response, username: str):
        """Edit user data."""
        resp.status = falcon.HTTP_200
        resp.media = {'msg': 'Not implemented yet.'}

    @falcon.before(IsAdminPermissionHook())
    def on_delete(self, req: Request, resp: Response, username: str):
        """Delete user. (set is_active=False)"""
        user = req.context.user

        user_to = self._user_crud_service.remove_user(user.licence_id, username=username)
        if user_to is None:
            raise falcon.HTTPNotFound(description=f'User {username} does not exist. [licence id = {user.licence_id}]')

        resp.status = falcon.HTTP_200
        resp.media = user_to.as_json()
