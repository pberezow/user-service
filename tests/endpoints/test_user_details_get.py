import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import USERS_DETAILS_PATH
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestUserDetailsGet(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)
        cls.user_to_get = create_non_admin_user(cls.services)
        cls.valid_fields = {'id', 'licence_id', 'username', 'email', 'is_admin', 'first_name', 'last_name',
                            'phone_number', 'address', 'position', 'last_login', 'date_joined', 'is_active', 'groups'}

    def test_get_user_by_admin_success(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_get(
            USERS_DETAILS_PATH % self.user_to_get.username,
            headers=auth_headers
        )
        print(res)
        assert res.status == falcon.HTTP_OK
        user = self.services.user_crud_service.get_user(self.user_to_get.licence_id, self.user_to_get.username)
        assert user is not None
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_get_user_by_non_admin_success(self):
        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_get(
            USERS_DETAILS_PATH % self.user_to_get.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        user = self.services.user_crud_service.get_user(self.user_to_get.licence_id, self.user_to_get.username)
        assert user is not None
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_get_user_with_diff_licence_fail(self):
        user_with_diff_licence = create_user_with_different_licence(self.services)

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_get(
            USERS_DETAILS_PATH % user_with_diff_licence.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_NOT_FOUND
        user = self.services.user_crud_service.get_user(self.user_to_get.licence_id, self.user_to_get.username)
        assert user is not None

    def test_get_inactive_user_by_admin_success(self):
        user = create_non_admin_user(self.services)
        if self.services.user_crud_service.remove_user(user.licence_id, user.username, hard_delete=False) is None:
            raise RuntimeError('Cannot set user inactive.')
        else:
            user.is_active = False

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_get(
            USERS_DETAILS_PATH % user.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_get_inactive_user_by_non_admin_fail(self):
        user = create_non_admin_user(self.services)
        if self.services.user_crud_service.remove_user(user.licence_id, user.username, hard_delete=False) is None:
            raise RuntimeError('Cannot set user inactive.')

        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_get(
            USERS_DETAILS_PATH % user.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_NOT_FOUND

    def test_get_user_by_unauthorized_fail(self):
        res = self.client.simulate_get(
            USERS_DETAILS_PATH % self.user_to_get.username
        )
        assert res.status == falcon.HTTP_UNAUTHORIZED
