import falcon
from typing import Dict

from tests.endpoints.utils.utils import ServicesContainer
from tests.endpoints.utils.paths import LOGIN_PATH
from tests.endpoints.utils.falcon_client import get_client_with_unique_db

from user_service.db import DBManager


class BaseTestEndpoint:
    client = None

    @staticmethod
    def setup_class(cls):
        # Clear database
        cls.client = get_client_with_unique_db()  # get_falcon_client()
        cls.services = ServicesContainer(
            db_manager=cls.get_db_manager(),
            user_crud_service=cls.client.app.user_crud_service,
            jwt_service=cls.client.app.jwt_service,
            auth_service=cls.client.app.auth_service,
            group_crud_service=cls.client.app.group_crud_service,
            reset_token_service=cls.client.app.reset_token_service
        )

    @classmethod
    def get_db_manager(cls):
        return cls.client.app._db_manager

    @staticmethod
    def teardown_class(cls):
        try:
            cls.get_db_manager()._drop_db()
        except DBManager.DBConnectionError:
            pass

    def login(self, username: str, password: str) -> Dict[str, str]:
        payload = {
            'username': username,
            'password': password
        }
        res = self.client.simulate_post(LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None
        return {
            'token': res.cookies['token'].value,
            'refresh_token': res.cookies['refresh_token'].value
        }

    @staticmethod
    def get_auth_header(jwt: str) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {jwt}'
        }