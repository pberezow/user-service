from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken

from django.utils.translation import gettext_lazy as _
from django.core import exceptions as django_exceptions
from django.http.response import Http404

# Global errors
SERVER_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'E000', 'Empty message')
UNAUTHORIZED_ERROR = (status.HTTP_401_UNAUTHORIZED, 'E001', 'Empty message')
NON_ADMIN_USER_ERROR = (status.HTTP_403_FORBIDDEN, 'E002', 'Empty message')
DATABASE_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'E003', 'Empty message')
INVALID_REQUEST_DATA = (status.HTTP_400_BAD_REQUEST, 'E004', 'Empty message')
NOT_FOUND_ERROR = (status.HTTP_404_NOT_FOUND, 'E005', 'Empty message')
PERMISSION_DENIED_ERROR = (status.HTTP_403_FORBIDDEN, 'E006', 'Empty message')

# Service specified errors
INVALID_CREDENTIALS = (status.HTTP_401_UNAUTHORIZED, 'E301', 'Empty message')  # Wrong username or password
INVALID_JWT = (status.HTTP_401_UNAUTHORIZED, 'E302', 'Empty message')  # JWT expired or malformed
INVALID_RESET_TOKEN = (status.HTTP_400_BAD_REQUEST, 'E303', 'Empty message')  # Reset token expired or doesn't match any user
USER_DOES_NOT_EXIST = (status.HTTP_404_NOT_FOUND, 'E304', 'Empty message')  # There is no user with corresponding id
INVALID_GROUP_NAME = (status.HTTP_400_BAD_REQUEST, 'E305', 'Empty message')  # Group with given name does not exists
USER_ALREADY_EXISTS = (status.HTTP_400_BAD_REQUEST, 'E306', 'Empty message')  # Duplication on username field (and email?)
GROUP_ALREADY_EXISTS = (status.HTTP_400_BAD_REQUEST, 'E307', 'Empty message')  # Duplication on (name, licence_id) pair
GROUP_DOES_NOT_EXIST = (status.HTTP_404_NOT_FOUND, 'E308', 'Empty message')

# Validation errors
VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E309', 'Empty message')
USERNAME_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E310', 'Empty message')
PASSWORD_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E311', 'Empty message')
LICENCE_ID_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E312', 'Empty message')
IS_ADMIN_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E313', 'Empty message')
FIRST_NAME_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E314', 'Empty message')
LAST_NAME_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E315', 'Empty message')
EMAIL_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E316', 'Empty message')
PHONE_NUMBER_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E317', 'Empty message')
ADDRESS_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E318', 'Empty message')
POSITION_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E319', 'Empty message')
IS_ACTIVE_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E320', 'Empty message')
OLD_PASSWORD_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E321', 'Empty message')
RESET_TOKEN_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E322', 'Empty message')
GROUP_NAME_VALIDATION_ERROR = (status.HTTP_400_BAD_REQUEST, 'E323', 'Empty message')


validation_errors_map = {
    'username': USERNAME_VALIDATION_ERROR,
    'password': PASSWORD_VALIDATION_ERROR,
    'licence_id': LICENCE_ID_VALIDATION_ERROR,
    'is_admin': IS_ADMIN_VALIDATION_ERROR,
    'first_name': FIRST_NAME_VALIDATION_ERROR,
    'last_name': LAST_NAME_VALIDATION_ERROR,
    'email': EMAIL_VALIDATION_ERROR,
    'phone_number': PHONE_NUMBER_VALIDATION_ERROR,
    'address': ADDRESS_VALIDATION_ERROR,
    'position': POSITION_VALIDATION_ERROR,
    'is_active': IS_ACTIVE_VALIDATION_ERROR,

    'old_password': OLD_PASSWORD_VALIDATION_ERROR,
    'token': RESET_TOKEN_VALIDATION_ERROR,

    'name': GROUP_NAME_VALIDATION_ERROR
}


class BaseAPIException(Exception):
    error = SERVER_ERROR

    def __init__(self, status_code=None, error_code=None, error_message=None):
        self.status_code = status_code or self.error[0]
        self.error_code = error_code or self.error[1]
        self.error_message = error_message or self.error[2]

    def __str__(self):
        return f'[{self.status_code}] {self.error_code} : {self.error_message}'


class Unauthorized(BaseAPIException):
    error = UNAUTHORIZED_ERROR


class OnlyForAdmin(BaseAPIException):
    error = NON_ADMIN_USER_ERROR


class DatabaseError(BaseAPIException):
    error = DATABASE_ERROR


class InvalidRequestData(BaseAPIException):
    error = INVALID_REQUEST_DATA


class PageNotFound(BaseAPIException):
    error = NOT_FOUND_ERROR


class PermissionDenied(BaseAPIException):
    error = PERMISSION_DENIED_ERROR


class InvalidCredentials(BaseAPIException):
    error = INVALID_CREDENTIALS


class InvalidJWT(BaseAPIException):
    error = INVALID_JWT


class InvalidResetToken(BaseAPIException):
    error = INVALID_RESET_TOKEN


class UserDoesNotExist(BaseAPIException):
    error = USER_DOES_NOT_EXIST


class InvalidGroupName(BaseAPIException):
    error = INVALID_GROUP_NAME


class UserAlreadyExists(BaseAPIException):
    error = USER_ALREADY_EXISTS


class GroupAlreadyExists(BaseAPIException):
    error = GROUP_ALREADY_EXISTS


class GroupDoesNotExist(BaseAPIException):
    error = GROUP_DOES_NOT_EXIST


class ValidationError(BaseAPIException):
    error = VALIDATION_ERROR

    def __init__(self, status_code=None, error_code=None, error_message=None):
        super().__init__(status_code, None, error_message)

        if isinstance(error_code, list):
            errors = []
            for err in error_code:
                if isinstance(err, str):
                    errors.append(err)
                elif isinstance(err, ValidationError):
                    if isinstance(err.error_code, list):
                        errors += err.error_code
                    elif isinstance(err.error_code, str):
                        errors.append(err.error_code)
                    else:
                        errors = self.error[1]
                        break
                else:
                    errors = self.error[1]
                    break
            self.error_code = errors
        elif isinstance(error_code, str):
            self.error_code = error_code
        else:
            pass


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = PageNotFound()
    elif isinstance(exc, exceptions.PermissionDenied) or isinstance(exc, django_exceptions.PermissionDenied):
        exc = PermissionDenied()
    elif isinstance(exc, exceptions.NotAuthenticated) or isinstance(exc, InvalidToken):
        exc = Unauthorized()
        # resp = Response(exc.error_code, status=exc.status_code)
        # resp.delete_cookie('token')
        # return resp
    elif isinstance(exc, exceptions.ValidationError):
        exc = ValidationError()

    elif isinstance(exc, exceptions.APIException):  # standard DRF error response
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    if isinstance(exc, BaseAPIException):
        set_rollback()
        return Response(exc.error_code, status=exc.status_code)

    return None
