import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import USERS_LIST_PATH
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestUserListGet(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)
        cls.other_users = [create_user_with_different_licence(
            cls.services, licence_id=i, is_admin=(i % 2 == 0)
        ) for i in range(1, 10)]

        cls.valid_fields = {'id', 'username', 'email', 'is_admin', 'first_name', 'last_name',
                            'phone_number', 'position', 'is_active'}

    def test_get_users_by_admin_success(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )
        res = self.client.simulate_get(
            USERS_LIST_PATH,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        result = res.json
        assert len(result) == 2
        result_keys = set()
        [result_keys.update(set(user.keys())) for user in result]
        assert result_keys == self.valid_fields

    def test_get_users_by_non_admin_success(self):
        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )
        res = self.client.simulate_get(
            USERS_LIST_PATH,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        result = res.json
        assert len(result) == 2
        result_keys = set()
        [result_keys.update(set(user.keys())) for user in result]
        assert result_keys == self.valid_fields

    def test_get_users_by_unauthorized_fail(self):
        res = self.client.simulate_get(
            USERS_LIST_PATH
        )
        assert res.status == falcon.HTTP_UNAUTHORIZED

    def test_get_users_by_admin_with_removed(self):
        user_to_delete = create_non_admin_user(self.services)
        self.services.user_crud_service.remove_user(user_to_delete.licence_id, user_to_delete.username,
                                                    hard_delete=False)

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )
        res = self.client.simulate_get(
            USERS_LIST_PATH,
            headers=auth_headers
        )
        self.services.user_crud_service.remove_user(user_to_delete.licence_id, user_to_delete.username,
                                                    hard_delete=True)
        assert res.status == falcon.HTTP_OK
        result = res.json
        assert len(result) == 3
        result_keys = set()
        [result_keys.update(set(user.keys())) for user in result]
        assert result_keys == self.valid_fields

    def test_get_only_active_users_by_non_admin(self):
        user_to_delete = create_non_admin_user(self.services)
        self.services.user_crud_service.remove_user(user_to_delete.licence_id, user_to_delete.username,
                                                    hard_delete=False)

        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )
        res = self.client.simulate_get(
            USERS_LIST_PATH,
            headers=auth_headers
        )
        self.services.user_crud_service.remove_user(user_to_delete.licence_id, user_to_delete.username,
                                                    hard_delete=True)
        assert res.status == falcon.HTTP_OK
        result = res.json
        assert len(result) == 2
        result_keys = set()
        [result_keys.update(set(user.keys())) for user in result]
        assert result_keys == self.valid_fields
