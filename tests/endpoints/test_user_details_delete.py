import falcon

from tests.endpoints.utils.base_test_endpoint import BaseTestEndpoint
from tests.endpoints.utils.paths import USERS_DETAILS_PATH
from tests.endpoints.utils.utils import (create_admin_user, create_non_admin_user, ADMIN_PASSWORD, NON_ADMIN_PASSWORD,
                                         create_user_with_different_licence)


class TestDetailsListDelete(BaseTestEndpoint):

    @staticmethod
    def setup_class(cls):
        super().setup_class(cls)
        # Create users
        cls.admin_user = create_admin_user(cls.services)
        cls.non_admin_user = create_non_admin_user(cls.services)

    def test_delete_non_admin_user_by_admin_success(self):
        non_admin = create_non_admin_user(self.services)

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_delete(
            USERS_DETAILS_PATH % non_admin.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        removed_user = self.services.user_crud_service.get_user(non_admin.licence_id, non_admin.username)
        assert removed_user is not None
        assert removed_user.is_active is False
        assert res.json is None

    def test_delete_admin_user_by_admin_success(self):
        admin = create_admin_user(self.services)

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_delete(
            USERS_DETAILS_PATH % admin.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_OK
        removed_user = self.services.user_crud_service.get_user(admin.licence_id, admin.username)
        assert removed_user is not None
        assert removed_user.is_active is False
        assert res.json is None

    def test_delete_user_with_diff_licence_by_admin_fail(self):
        other_user = create_user_with_different_licence(self.services, licence_id=self.admin_user.licence_id+1)

        auth_headers = self.get_auth_header(
            self.login(self.admin_user.username, ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_delete(
            USERS_DETAILS_PATH % other_user.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_NOT_FOUND
        removed_user = self.services.user_crud_service.get_user(other_user.licence_id, other_user.username)
        assert removed_user is not None
        assert removed_user.is_active is True
        assert res.json is None

    def test_delete_user_by_non_admin_fail(self):
        non_admin = create_non_admin_user(self.services)

        auth_headers = self.get_auth_header(
            self.login(self.non_admin_user.username, NON_ADMIN_PASSWORD)['token']
        )

        res = self.client.simulate_delete(
            USERS_DETAILS_PATH % non_admin.username,
            headers=auth_headers
        )
        assert res.status == falcon.HTTP_FORBIDDEN
        removed_user = self.services.user_crud_service.get_user(non_admin.licence_id, non_admin.username)
        assert removed_user is not None
        assert removed_user.is_active is True

    def test_delete_user_by_unauthorized_fail(self):
        non_admin = create_non_admin_user(self.services)

        res = self.client.simulate_delete(
            USERS_DETAILS_PATH % non_admin.username
        )
        assert res.status == falcon.HTTP_UNAUTHORIZED
        removed_user = self.services.user_crud_service.get_user(non_admin.licence_id, non_admin.username)
        assert removed_user is not None
        assert removed_user.is_active is True
