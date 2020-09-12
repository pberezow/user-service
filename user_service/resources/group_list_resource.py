import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.mappers import GroupMapper
from user_service.services import GroupCRUDService
from user_service.hooks import IsAdminPermissionHook


class GroupListResource(BaseResource):
    """
    Provides group resource for operations on multiple groups and creating group.

    on_get - returns list of groups with same licence_id
    on post - creates new group
    """
    mapper = GroupMapper(included_attributes={'licence_id', 'name'})

    def __init__(self, group_crud_service: GroupCRUDService):
        self._group_crud_service = group_crud_service
        super().__init__()

    def on_get(self, req: Request, resp: Response):
        user = req.context.user

        groups_to = self._group_crud_service.get_groups_for_licence(user.licence_id)
        resp.status = falcon.HTTP_200
        resp.media = [g.as_json() for g in groups_to]

    @falcon.before(IsAdminPermissionHook())
    def on_post(self, req: Request, resp: Response):
        user = req.context.user

        data = req.media or {}
        data['licence_id'] = user.licence_id

        group_to = self.map_with_error(data)
        # TODO - catch exceptions
        group_to = self._group_crud_service.create_group(group_to)

        resp.status = falcon.HTTP_200
        resp.media = group_to.as_json()
