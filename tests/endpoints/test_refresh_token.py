import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import LOGIN_PATH, REFRESH_TOKEN_PATH
from tests.endpoints.utils.utils import create_admin_user, ADMIN_PASSWORD


class TestRefreshToken(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.user = create_admin_user(cls.services)

    def _login(self):
        payload = {
            'username': self.user.username,
            'password': ADMIN_PASSWORD
        }
        res = self.client.simulate_post(LOGIN_PATH, json=payload)
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None
        return {
            'token': res.cookies['token'].value,
            'refresh_token': res.cookies['refresh_token'].value
        }

    def test_refresh_success(self):
        tokens = self._login()
        res = self.client.simulate_post(
            REFRESH_TOKEN_PATH,
            json={'refresh_token': tokens['refresh_token']}
        )
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None

    def test_refresh_wrong_token_failed(self):
        tokens = self._login()
        res = self.client.simulate_post(
            REFRESH_TOKEN_PATH,
            json={'refresh_token': tokens['token']}
        )
        assert res.status == falcon.HTTP_BAD_REQUEST
        assert res.cookies.get('token', None) is None
        assert res.cookies.get('refresh_token', None) is None

    def test_refresh_empty_payload(self):
        tokens = self._login()
        res = self.client.simulate_post(
            REFRESH_TOKEN_PATH,
            json={}
        )
        assert res.status == falcon.HTTP_BAD_REQUEST
        assert res.cookies.get('token', None) is None
        assert res.cookies.get('refresh_token', None) is None

    def test_refresh_malformed_token(self):
        tokens = self._login()
        malformed_token = 'asd' + tokens['refresh_token']
        res = self.client.simulate_post(
            REFRESH_TOKEN_PATH,
            json={'refresh_token': malformed_token}
        )
        print(res.cookies)
        assert res.status == falcon.HTTP_BAD_REQUEST
        assert res.cookies.get('token', None) is None
        assert res.cookies.get('refresh_token', None) is None
