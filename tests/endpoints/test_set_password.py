import falcon
import time

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import SET_PASSWORD_PATH, LOGIN_PATH
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestSetPassword(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)
        cls.new_password = 'new_password123'

    def test_set_password_admin_success(self):
        user = create_admin_user(self.services)
        auth_headers = self.get_auth_header(
            self.login(user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            SET_PASSWORD_PATH % user.username,
            json={'old_password': ADMIN_PASSWORD, 'password': self.new_password},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK

        self.login(user.username, self.new_password)

    def test_set_password_non_admin_success(self):
        user = create_non_admin_user(self.services)
        auth_headers = self.get_auth_header(
            self.login(user.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            SET_PASSWORD_PATH % user.username,
            json={'old_password': NON_ADMIN_PASSWORD, 'password': self.new_password},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK

        self.login(user.username, self.new_password)

    def test_set_password_wrong_old_password_fail(self):
        user = create_admin_user(self.services)
        auth_headers = self.get_auth_header(
            self.login(user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            SET_PASSWORD_PATH % user.username,
            json={'old_password': 'wrong_password', 'password': self.new_password},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_set_password_missing_old_password_fail(self):
        user = create_admin_user(self.services)
        auth_headers = self.get_auth_header(
            self.login(user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            SET_PASSWORD_PATH % user.username,
            json={'password': self.new_password},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_set_password_of_other_user_fail(self):
        user = create_admin_user(self.services)
        auth_headers = self.get_auth_header(
            self.login(user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            SET_PASSWORD_PATH % self.admin_user.username,
            json={'old_password': ADMIN_PASSWORD, 'password': self.new_password},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_FORBIDDEN
