import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import LOGIN_PATH
from tests.endpoints.utils.utils import create_non_admin_user, create_admin_user, NON_ADMIN_PASSWORD, ADMIN_PASSWORD


class TestLoginEndpoint(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)

    @staticmethod
    def teardown_class(cls):
        super().teardown_class(cls)
        pass

    def test_login_admin_success(self):
        payload = {
            'username': self.admin_user.username,
            'password': ADMIN_PASSWORD
        }
        res = self.client.simulate_post(path=LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None

    def test_login_non_admin_success(self):
        payload = {
            'username': self.non_admin_user.username,
            'password': NON_ADMIN_PASSWORD
        }
        res = self.client.simulate_post(path=LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None

    def test_login_admin_fail(self):
        payload = {
            'username': self.admin_user.username,
            'password': 'wrong_password'
        }
        res = self.client.simulate_post(path=LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_UNAUTHORIZED
        assert res.cookies.get('token', None) is None
        assert res.cookies.get('refresh_token', None) is None

    def test_login_non_admin_fail(self):
        payload = {
            'username': self.non_admin_user.username,
            'password': 'wrong_password'
        }
        res = self.client.simulate_post(path=LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_UNAUTHORIZED
        assert res.cookies.get('token', None) is None
        assert res.cookies.get('refresh_token', None) is None
