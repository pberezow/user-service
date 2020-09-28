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

ADMIN_PASSWORD = 'adminpassword'
NON_ADMIN_PASSWORD = 'nonadminpassword'


def create_admin_user(services: ServicesContainer):
    data = {
        **_user_default_params,
        'is_admin': True,
        'username': 'admin_user',
        'password': ADMIN_PASSWORD,
        'email': 'admin_user@sili.com',
        'licence_id': 0
    }
    return services.user_crud_service.create_user(UserTO(**data))


def create_non_admin_user(services: ServicesContainer):
    data = {
        **_user_default_params,
        'is_admin': False,
        'username': 'non_admin_user',
        'password': NON_ADMIN_PASSWORD,
        'email': 'non_admin_user@sili.com',
        'licence_id': 0
    }
    return services.user_crud_service.create_user(UserTO(**data))
