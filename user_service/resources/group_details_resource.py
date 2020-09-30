import falcon
from falcon import Response, Request

from user_service.utils import BaseResource
from user_service.services import GroupCRUDService
from user_service.mappers import GroupMapper
from user_service.hooks import IsAdminPermissionHook, IsSelfPermissionHook, OrPermissionsHook


class GroupDetailsResource(BaseResource):
    """
    Provides group resource with actions on specific group. (distinguished by name)

    on_get - returns details about group.
    on_put - changes group's data.
    on_delete - removes group
    """
    mapper = GroupMapper(included_attributes={'name'})

    def __init__(self, group_crud_service: GroupCRUDService):
        self._group_crud_service = group_crud_service
        super().__init__()

    def on_get(self, req: Request, resp: Response, group_name: str):
        """Get group by name."""
        user = req.context.user

        group_to = self._group_crud_service.get_group(user.licence_id, name=group_name)
        if group_to is None:
            raise falcon.HTTPNotFound(
                description=f'Group {group_name} does not exist. [licence id = {user.licence_id}]'
            )

        resp.status = falcon.HTTP_200
        resp.media = group_to.as_json()

    @falcon.before(IsAdminPermissionHook())
    def on_put(self, req: Request, resp: Response, group_name: str):
        """Edit group data."""
        resp.status = falcon.HTTP_200
        resp.media = {'msg': 'Not implemented yet.'}

    @falcon.before(IsAdminPermissionHook())
    def on_delete(self, req: Request, resp: Response, group_name: str):
        """Delete group."""
        user = req.context.user

        group_to = self._group_crud_service.remove_group(user.licence_id, name=group_name)
        if group_to is None:
            raise falcon.HTTPNotFound(
                description=f'Group {group_name} does not exist. [licence id = {user.licence_id}]'
            )

        resp.status = falcon.HTTP_200
        resp.media = group_to.as_json()
