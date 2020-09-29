import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import USERS_DETAILS_PATH
from tests.endpoints.utils.utils import create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD


class TestUserListCreate(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)

        cls.users_data = {
            'admin_payload': {
                'username': 'new_admin_user',
                'email': 'asd@asd.asd',
                'password': 'new_admin_password123',
                'is_admin': True
            },
            'user_payload': {
                'username': 'new_non_admin_user',
                'email': 'asd1@asd.asd',
                'password': 'new_non_admin_password123',
                'is_admin': False
            }
        }

    def setup_method(self):
        self.users = []

    def teardown_method(self):
        for user in self.users:
            removed_user = self.services.user_crud_service.remove_user(user['licence_id'], user['username'], hard_delete=True)
            if removed_user is None:
                raise RuntimeError(f'Error while removing user -> {user["username"]}  ({user["licence_id"]})')

    def test_create_user_by_admin_success(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['admin_payload'],
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_CREATED
        user_to = self.services.user_crud_service.get_user(
            licence_id=self.admin_user.licence_id,
            username=self.users_data['admin_payload']['username'])
        assert user_to is not None

        self.users.append({**self.users_data['admin_payload'], 'licence_id': self.admin_user.licence_id})

        params_to_check = {**self.users_data['admin_payload']}
        del params_to_check['password']
        for k, v in params_to_check.items():
            assert getattr(user_to, k) == v

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['user_payload'],
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_CREATED
        user_to = self.services.user_crud_service.get_user(
            licence_id=self.admin_user.licence_id,
            username=self.users_data['user_payload']['username'])
        assert user_to is not None

        self.users.append({**self.users_data['user_payload'], 'licence_id': self.admin_user.licence_id})

        params_to_check = {**self.users_data['user_payload']}
        del params_to_check['password']
        for k, v in params_to_check.items():
            assert getattr(user_to, k) == v

    def test_create_same_user_twice_fail(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['admin_payload'],
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_CREATED
        self.users.append({**self.users_data['admin_payload'], 'licence_id': self.admin_user.licence_id})

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['admin_payload'],
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_create_user_with_different_licence_id(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json={**self.users_data['admin_payload'], 'licence_id': self.admin_user.licence_id+10},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_CREATED
        self.users.append({**self.users_data['admin_payload'], 'licence_id': self.admin_user.licence_id})

        user_to = self.services.user_crud_service.get_user(
            licence_id=self.admin_user.licence_id,
            username=self.users_data['admin_payload']['username'])
        assert user_to is not None
        assert user_to.licence_id == self.admin_user.licence_id

    def test_create_user_by_admin_wrong_payload_fail(self):
        wrong_payload = {
            'username': 'new_admin_user',
            'email': 'asd@asd.asd',
            'password': 'new_admin_password123',
            'is_admin': 'True'
        }
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=wrong_payload,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_create_user_by_admin_empty_payload_fail(self):
        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json={},
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_create_user_by_non_admin_fail(self):
        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['user_payload'],
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_FORBIDDEN

    def test_create_user_by_unauthorized_fail(self):
        res = self.client.simulate_post(
            USERS_DETAILS_PATH,
            json=self.users_data['user_payload']
        )
        assert res.status == falcon.HTTP_UNAUTHORIZED
