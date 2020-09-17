import falcon
from falcon import Request, Response

from user_service.utils import BaseResource
from user_service.mappers import UserMapper
from user_service.mappers.flat_group_mapper import FlatGroupMapper
from user_service.services import UserCRUDService
from user_service.hooks import IsAdminPermissionHook


class UserGroupsResource(BaseResource):
    mapper = UserMapper(included_attributes={'groups'},
                        nested_validators={
                            'groups': FlatGroupMapper(many=True, included_attributes={'name'})
                        })

    def __init__(self, user_crud_service: UserCRUDService):
        self._user_crud_service = user_crud_service
        super().__init__()

    @falcon.before(IsAdminPermissionHook())
    def on_put(self, req: Request, resp: Response, username: str):
        user = req.context.user
        data = req.media
        print('Validating input...')
        user_to = self.map_with_error(data)
        print(f'OK.\nSetting groups for {username}...')

        user_to = self._user_crud_service.set_user_groups(
            licence_id=user.licence_id,
            username=username,
            groups_names=[g.name for g in user_to.groups]
        )
        print(f'Ok. {user_to}')

        if user_to is None:
            raise falcon.HTTPBadRequest()

        resp.status = falcon.HTTP_200
        resp.media = user_to.as_json()
