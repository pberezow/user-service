import falcon
from datetime import datetime
from user_service.db import DBManager
from user_service.repository import UserRepository, GroupRepository, ResetTokenRepository
from user_service.services import UserCRUDService, AuthService, JWTService, GroupCRUDService, ResetTokenService
from user_service.resources import (UserDetailsResource, UserListResource, LoginResource, LogoutResource,
                                    RefreshTokenResource, SetPasswordResource, GroupDetailsResource,
                                    GroupListResource, UserGroupsResource, ValidateResetTokenResource,
                                    ResetPasswordResource, CreateResetTokenResource)
from user_service.middlewares import AuthMiddleware, RequestTimeMiddleware
from user_service.models.user import UserTO
from user_service.exceptions.database import DatabaseException


class UserApplication(falcon.API):
    def __init__(self, config, router=None, independent_middleware=True, debug=False, init_db=False):
        self.config = config
        self._debug = debug

        self._setup_db(init_db=init_db)
        self._setup_services()

        middleware = self._setup_middleware()
        super().__init__(middleware=middleware, router=router, independent_middleware=independent_middleware)
        self._setup_routes()

        if init_db:
            self._create_admins()

    def _setup_db(self, init_db=False):
        self._db_manager = DBManager(db_config=self.config['db'], init_db=init_db,
                                     init_script=self.config.get('db_init_script', None))
        self._db_manager.setup()
        self.user_repository = UserRepository(self._db_manager)
        self.group_repository = GroupRepository(self._db_manager)
        self.reset_token_repository = ResetTokenRepository(self._db_manager)

    def _setup_services(self):
        self.user_crud_service = UserCRUDService(
            self.user_repository,
            self.group_repository
        )
        jwt_cfg = self.config['jwt']
        self.jwt_service = JWTService(
            jwt_cfg['private_key'],
            jwt_cfg['public_key'],
            jwt_cfg['issuer'],
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
        self.reset_token_service = ResetTokenService(
            self.reset_token_repository,
            self.user_repository,
            self.user_crud_service,
            self.config['reset_password_token_lifetime']
        )

    def _setup_routes(self):
        self.add_route('/login', LoginResource(self.auth_service, self.jwt_service))
        self.add_route('/logout', LogoutResource())
        self.add_route('/refresh', RefreshTokenResource(self.jwt_service, self.auth_service))

        self.add_route('/reset', ResetPasswordResource(self.reset_token_service))
        self.add_route('/reset/token', CreateResetTokenResource(self.reset_token_service))
        self.add_route('/reset/token/validate', ValidateResetTokenResource(self.reset_token_service))

        self.add_route('/', UserListResource(self.user_crud_service))
        self.add_route('/{username}', UserDetailsResource(self.user_crud_service))
        self.add_route('/{username}/password', SetPasswordResource(self.user_crud_service, self.auth_service))
        self.add_route('/{username}/permissions', UserGroupsResource(self.user_crud_service))

        self.add_route('/permissions', GroupListResource(self.group_crud_service))
        self.add_route('/permissions/{group_name}', GroupDetailsResource(self.group_crud_service))

    def _setup_middleware(self):
        middleware = [
            AuthMiddleware(self.jwt_service,
                           {'/login', '/refresh', '/reset', '/reset/token', '/reset/token/validate'})
        ]

        if self._debug:
            middleware = [RequestTimeMiddleware(), *middleware]

        return middleware

    def _create_admins(self):
        print('Creating admins...')
        defaults = {
            'licence_id': 0,
            'is_admin': True,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'address': '',
            'position': 'Sili Admin',
            'is_active': True,
            'date_joined': datetime.now(),
            'last_login': None
        }

        for admin in self.config.get('admins', {}):
            try:
                print(f'Creating admin: {admin["username"]}/{admin["password"]}  -->  ', end='')
                data = {**defaults, **admin}
                user_to = UserTO(**data)
                user_to = self.user_crud_service.create_user(user_to)
                print('Success')
            except DatabaseException as err:
                print('Failed')
                err.print_diag()
