import falcon
from user_service.db import DBManager
from user_service.repository import UserRepository, GroupRepository
from user_service.services import UserCRUDService, AuthService, JWTService, GroupCRUDService
from user_service.resources import (UserDetailsResource, UserListResource, LoginResource, LogoutResource,
                                    RefreshTokenResource, SetPasswordResource, GroupDetailsResource,
                                    GroupListResource, UserGroupsResource)
from user_service.middlewares import AuthMiddleware, RequestTimeMiddleware
from user_service.models.user import UserTO


class UserApplication(falcon.API):
    def __init__(self, config, router=None, independent_middleware=True, debug=False):
        self.config = config
        self._debug = debug

        self._setup_db()
        self._setup_services()

        middleware = self._setup_middleware()
        super().__init__(middleware=middleware, router=router, independent_middleware=independent_middleware)
        self._setup_routes()
        self._create_admins()

    def _setup_db(self):
        self._db_manager = DBManager(db_config=self.config['db'])
        self._db_manager.setup()
        self.user_repository = UserRepository(self._db_manager)
        self.group_repository = GroupRepository(self._db_manager)

    def _setup_services(self):
        self.user_crud_service = UserCRUDService(
            self.user_repository,
            self.group_repository
        )
        jwt_cfg = self.config['jwt']
        self.jwt_service = JWTService(
            jwt_cfg['private_key'],
            jwt_cfg['public_key'],
            jwt_cfg['algorithm'],
            jwt_cfg['token_lifetime'],
            jwt_cfg['refresh_secret'],
            jwt_cfg['refresh_token_lifetime']
        )
        self.auth_service = AuthService(
            self.user_repository
        )
        self.group_crud_service = GroupCRUDService(
            self.group_repository,
            self.user_repository
        )

    def _setup_routes(self):
        self.add_route('/login', LoginResource(self.auth_service, self.jwt_service))
        self.add_route('/logout', LogoutResource())
        self.add_route('/refresh', RefreshTokenResource(self.jwt_service, self.auth_service))

        self.add_route('/', UserListResource(self.user_crud_service))
        self.add_route('/{username}', UserDetailsResource(self.user_crud_service))
        self.add_route('/{username}/password', SetPasswordResource(self.user_crud_service, self.auth_service))
        self.add_route('/{username}/permissions', UserGroupsResource(self.user_crud_service))

        self.add_route('/permissions', GroupListResource(self.group_crud_service))
        self.add_route('/permissions/{group_name}', GroupDetailsResource(self.group_crud_service))

    def _setup_middleware(self):
        middleware = [
            AuthMiddleware(self.jwt_service, {'/login', '/refresh'})
        ]

        if self._debug:
            middleware = [RequestTimeMiddleware(), *middleware]

        return middleware

    def _create_admins(self):
        defaults = {
            'licence_id': 0,
            'is_admin': True,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': 'Sili Admin'
        }

        for admin in self.config.get('admins', {}):
            try:
                print(f'Creating admin: {admin["username"]}/{admin["password"]}')
                data = {**defaults, **admin}
                user_to = UserTO(**data)
                user_to = self.user_crud_service.create_user(user_to)
                print('Success')
            except Exception as err:
                print('Failed')
                print(err)
