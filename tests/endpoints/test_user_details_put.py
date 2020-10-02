import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import USERS_DETAILS_PATH
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestUserDetailsPut(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)
        cls.valid_fields = {'id', 'licence_id', 'username', 'email', 'is_admin', 'first_name', 'last_name',
                            'phone_number', 'address', 'position', 'last_login', 'date_joined', 'is_active', 'groups'}

    def test_set_all_attributes_of_other_user_by_admin_success(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['username', 'email', 'is_admin', 'first_name', 'last_name', 'phone_number', 'address',
                             'position']

        values = ['userA', 'userA@sili.com', True, 'UserA', 'UserA', '000000000', 'UserA', 'UserA']

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        assert res.status == falcon.HTTP_OK
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=values[0])
        assert user is not None
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_set_all_attributes_of_self_by_admin_success(self):
        user_to_set = create_admin_user(self.services)

        attributes_to_set = ['username', 'email', 'is_admin', 'first_name', 'last_name', 'phone_number', 'address',
                             'position']

        values = ['userAA', 'userAA@sili.com', True, 'UserAA', 'UserAA', '000000000', 'UserAA', 'UserAA']

        auth_headers = self.get_auth_header(
            self.login(user_to_set.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        assert res.status == falcon.HTTP_OK
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=values[0])
        assert user is not None
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_set_invalid_attributes_of_other_user_by_admin_fail(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['username', 'email', 'is_admin', 'first_name', 'last_name', 'phone_number', 'address',
                             'position', 'password']

        values = ['userAAA', 'userAAA@sili.com', True, 'UserAAA', 'UserAAA', '000000000', 'UserAAA', 'UserAAA',
                  'new_password']

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        assert res.status == falcon.HTTP_BAD_REQUEST
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=values[0])
        assert user is None

    def test_set_wrong_value_of_email_fail(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['email']

        values = ['userAAA@@sili.com']

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )
        print(res.json)
        assert res.status == falcon.HTTP_BAD_REQUEST
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=user_to_set.username)
        assert user is not None
        assert user.email != values[0]

    def test_set_username_same_as_other_users_fail(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['username']

        values = [self.admin_user.username]

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_set_attributes_of_self_by_non_admin_success(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['email', 'first_name', 'last_name', 'phone_number', 'address']

        values = ['userAAAA@sili.com', 'UserAAAA', 'UserAAAA', '000000000', 'UserAAAA']

        auth_headers = self.get_auth_header(
            self.login(user_to_set.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        assert res.status == falcon.HTTP_OK
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=user_to_set.username)
        assert user is not None
        user = user.as_json()
        for k, v in res.json.items():
            assert v == user[k]
        assert self.valid_fields == set(res.json.keys())

    def test_set_restricted_attributes_of_self_by_non_admin_fail(self):
        user_to_set = create_non_admin_user(self.services)

        attributes_to_set = ['username', 'is_admin', 'position']

        values = ['userAAAAA', True, 'UserAAAAA']

        auth_headers = self.get_auth_header(
            self.login(user_to_set.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        # just like empty request
        assert res.status == falcon.HTTP_BAD_REQUEST
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=values[0])
        assert user is None
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, username=user_to_set.username)
        assert user is not None
        user = user.as_json()
        for k, v in zip(attributes_to_set, values):
            assert v != user[k]

    def test_set_attributes_of_user_with_diff_licence_by_admin_fail(self):
        user_to_set = create_user_with_different_licence(self.services)

        attributes_to_set = ['first_name', 'last_name']

        values = ['First', 'Last']

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_put(
            USERS_DETAILS_PATH % user_to_set.username,
            json=dict(zip(attributes_to_set, values)),
            headers=auth_headers
        )

        assert res.status == falcon.HTTP_NOT_FOUND
        user = self.services.user_crud_service.get_user(user_to_set.licence_id, user_to_set.username)
        assert user is not None
