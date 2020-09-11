import pytest

from user_service.utils.validators import (get_str_len_validator, get_type_validator, phone_number_validator,
                                           email_validator)


class TestTypeValidator:

    def test_single_type_success(self):
        validator = get_type_validator(str)
        result = validator('example_str')
        assert result is True

    def test_single_type_fail(self):
        validator = get_type_validator(str)
        result = validator(10)
        assert result is False

    def test_multiple_types_success(self):
        validator = get_type_validator(str, int)
        result = validator('example_str')
        assert result is True
        result = validator(10)
        assert result is True

    def test_multiple_types_fail(self):
        validator = get_type_validator(str, int)
        result = validator(type(None))
        assert result is False
        result = validator(10.1)
        assert result is False

    def test_validation_for_test_class(self):
        class TestClass:
            pass

        class TestClass2(TestClass):
            pass

        validator = get_type_validator(TestClass)
        result = validator(TestClass())
        assert result is True
        result = validator(TestClass2())
        assert result is False

        validator = get_type_validator(TestClass2)
        result = validator(TestClass2())
        assert result is True
        result = validator(TestClass())
        assert result is False


class TestStrLenValidator:

    def test_only_min_len_validator_success(self):
        validator = get_str_len_validator(min_length=10)
        result = validator('a' * 10)
        assert result is True
        result = validator('a' * 15)
        assert result is True

    def test_only_min_len_validator_fail(self):
        validator = get_str_len_validator(min_length=10)
        result = validator('a' * 9)
        assert result is False
        result = validator('')
        assert result is False

    def test_only_max_len_validator_success(self):
        validator = get_str_len_validator(max_length=10)
        result = validator('a' * 10)
        assert result is True
        result = validator('')
        assert result is True

    def test_only_max_len_validator_fail(self):
        validator = get_str_len_validator(max_length=10)
        result = validator('a' * 20)
        assert result is False
        result = validator('a' * 300)
        assert result is False

    def test_min_max_len_validator_success(self):
        validator = get_str_len_validator(min_length=10, max_length=20)
        result = validator('a' * 10)
        assert result is True
        result = validator('a' * 15)
        assert result is True
        result = validator('a' * 20)
        assert result is True

    def test_min_max_len_validator_fail(self):
        validator = get_str_len_validator(min_length=10, max_length=20)
        result = validator('a' * 9)
        assert result is False
        result = validator('')
        assert result is False
        result = validator('a' * 21)
        assert result is False


class TestEmailValidator:

    def test_correct_emails_success(self):
        emails = ['asd@asd.asd', 'ASD.asd-qwe@vvqev.qdw.qw', '123ASD.asd-qwe123@v5vqev.qdw.qw']
        for email in emails:
            assert email_validator(email) is True

    def test_incorrect_emails_fail(self):
        emails = ['', '@.pl', '.@..pl', 'asd@@asd.pl', 'qwe@qwe', '@qwe.xq', 'asd@asd.z', 'asdascqw.qw']
        for email in emails:
            assert email_validator(email) is False


class TestPhoneNumberValidator:

    def test_phone_number_validator_success(self):
        numbers = ['123123123', '+48123123123', '+11231231234', '1231231234']
        for number in numbers:
            assert phone_number_validator(number) is True

    def test_phone_number_validator_fail(self):
        numbers = ['++123123123', '12312312', 'asdasdasd', '+123+123123123']
        for number in numbers:
            assert phone_number_validator(number) is False
