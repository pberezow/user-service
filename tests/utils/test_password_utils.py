import pytest

from user_service.utils.password_utils import is_password_valid, hash_password


class TestHashPassword:

    def test_valid_password_type(self):
        raw_password = 'secure_password'
        h = hash_password(raw_password)
        assert h != raw_password
        assert type(h) == str

    def test_invalid_password_type(self):
        raw_passwords = [b'secure_password', 123456678]
        for raw_password in raw_passwords:
            try:
                h = hash_password(raw_password)
                assert False
            except Exception:
                assert True


class TestIsPasswordValid:

    def test_validation_success(self):
        raw_password = 'secure_password'
        h = hash_password(raw_password)
        assert is_password_valid(raw_password, h) is True

    def test_validation_fail(self):
        raw_password = 'secure_password'
        h = hash_password(raw_password)
        assert is_password_valid('another_password', h) is False
