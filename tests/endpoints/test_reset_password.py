import falcon
import time

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import (CREATE_RESET_TOKEN_PATH, RESET_PASSWORD_PATH, VALIDATE_RESET_TOKEN_PATH,
                                         LOGIN_PATH)
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestResetPassword(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)
        cls.max_token_creation_time = 3

    def test_reset_password_path_success(self):
        # GENERATE TOKEN
        res = self.client.simulate_post(
            CREATE_RESET_TOKEN_PATH,
            json={'email': self.admin_user.email}
        )
        assert res.status == falcon.HTTP_OK
        time.sleep(self.max_token_creation_time)

        try:
            reset_token = self.services.reset_token_service._reset_token_repository.get_token_for_user_id(
                self.admin_user.id
            )
        except Exception:
            raise RuntimeError(f'Token creation time is greater than {self.max_token_creation_time} sec.')

        # VALIDATE TOKEN
        res = self.client.simulate_post(
            VALIDATE_RESET_TOKEN_PATH,
            json={'token': reset_token}
        )
        assert res.status == falcon.HTTP_OK
        assert res.json.get('is_valid', None) is True

        # RESET PASSWORD
        new_password = 'new_password123'
        res = self.client.simulate_post(
            RESET_PASSWORD_PATH,
            json={'token': reset_token, 'password': new_password}
        )
        assert res.status == falcon.HTTP_OK

        # TRY TO LOG IN
        res = self.client.simulate_post(
            LOGIN_PATH,
            json={'username': self.admin_user.username, 'password': new_password}
        )
        assert res.status == falcon.HTTP_OK
        assert res.cookies.get('token', None) is not None
        assert res.cookies.get('refresh_token', None) is not None

    def test_validation_of_invalid_token(self):
        invalid_token = 'some token'
        res = self.client.simulate_post(
            VALIDATE_RESET_TOKEN_PATH,
            json={'token': invalid_token}
        )
        assert res.status == falcon.HTTP_OK
        assert res.json.get('is_valid', None) is False

    def test_validation_with_empty_payload(self):
        res = self.client.simulate_post(
            VALIDATE_RESET_TOKEN_PATH,
            json={}
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_reset_password_with_invalid_token(self):
        invalid_token = 'some token'
        res = self.client.simulate_post(
            RESET_PASSWORD_PATH,
            json={'token': invalid_token, 'password': 'some new password123'}
        )
        assert res.status == falcon.HTTP_BAD_REQUEST

    def test_create_token_endpoint_with_wrong_email(self):
        res = self.client.simulate_post(
            CREATE_RESET_TOKEN_PATH,
            json={'email': 'wrong_email@asd.qw'}
        )
        assert res.status == falcon.HTTP_OK
