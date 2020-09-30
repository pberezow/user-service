from datetime import datetime

from user_service.models import UserTO
from user_service.db import DBManager


# class ServicesContainer(metaclass=Singleton):
class ServicesContainer:
    def __init__(self, db_manager: DBManager, **kwargs):
        self.db_manager = db_manager
        for k, v in kwargs.items():
            setattr(self, k, v)


_user_default_params = {
    'is_active': True,
    'last_login': None,
    'date_joined': datetime.now(),
    'first_name': 'Firstname',
    'last_name': 'Lastname',
    'phone_number': '123456789',
    'address': 'default address',
    'position': 'default_position'
}

ADMIN_PASSWORD = 'adminpassword123'
NON_ADMIN_PASSWORD = 'nonadminpassword123'
NON_SILI_PASSWORD = 'nonsilipassword123'


def _create_admin_user():
    indices = [0]

    def func(services: ServicesContainer) -> UserTO:
        indices.append(indices[-1]+1)
        data = {
            **_user_default_params,
            'is_admin': True,
            'username': f'admin_user{indices[-1]}',
            'password': ADMIN_PASSWORD,
            'email': f'admin_user{indices[-1]}@sili.com',
            'licence_id': 0
        }
        user_to = services.user_crud_service.create_user(UserTO(**data))
        if user_to is None:
            raise RuntimeError('Cannot create admin user.')
        return user_to

    return func


create_admin_user = _create_admin_user()


def _create_non_admin_user():
    indices = [0]

    def func(services: ServicesContainer) -> UserTO:
        indices.append(indices[-1]+1)
        data = {
            **_user_default_params,
            'is_admin': False,
            'username': f'non_admin_user{indices[-1]}',
            'password': NON_ADMIN_PASSWORD,
            'email': f'non_admin_user{indices[-1]}@sili.com',
            'licence_id': 0
        }
        user_to = services.user_crud_service.create_user(UserTO(**data))
        if user_to is None:
            raise RuntimeError('Cannot create non admin user.')
        return user_to

    return func


create_non_admin_user = _create_non_admin_user()


def _create_user_with_different_licence():
    indices = [0]

    def func(service: ServicesContainer, licence_id: int = 1, is_admin: bool = False) -> UserTO:
        indices.append(indices[-1]+1)
        data = {
            **_user_default_params,
            'is_admin': is_admin,
            'username': f'non_sili_user{indices[-1]}',
            'password': NON_SILI_PASSWORD,
            'email': f'user{indices[-1]}@non_sili.com',
            'licence_id': licence_id
        }
        user_to = service.user_crud_service.create_user(UserTO(**data))
        if user_to is None:
            raise RuntimeError(f'Cannot create user licence_id = {licence_id}.')
        return user_to

    return func


create_user_with_different_licence = _create_user_with_different_licence()
