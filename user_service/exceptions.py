from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status

from django.utils.translation import gettext_lazy as _
from django.core import exceptions as django_exceptions
from django.http.response import Http404


SERVER_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'E000', 'Empty message')
UNAUTHORIZED_ERROR = (status.HTTP_401_UNAUTHORIZED, 'E001', 'Empty message')
NON_ADMIN_USER_ERROR = (status.HTTP_403_FORBIDDEN, 'E002', 'Empty message')
DATABASE_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'E003', 'Empty message')
INVALID_REQUEST_DATA = (status.HTTP_400_BAD_REQUEST, 'E004', 'Empty message')
NOT_FOUND_ERROR = (status.HTTP_404_NOT_FOUND, 'E005', 'Empty message')
PERMISSION_DENIED_ERROR = (status.HTTP_403_FORBIDDEN, 'E006', 'Empty message')

INVALID_CREDENTIALS = (status.HTTP_401_UNAUTHORIZED, 'E301', 'Empty message')  # Wrong username or password
INVALID_JWT = (status.HTTP_401_UNAUTHORIZED, 'E302', 'Empty message')  # JWT expired or malformed
INVALID_RESET_TOKEN = (status.HTTP_400_BAD_REQUEST, 'E303', 'Empty message')  # Reset token expired or doesn't match any user
USER_DOES_NOT_EXIST = (status.HTTP_404_NOT_FOUND, 'E304', 'Empty message')  # There is no user with corresponding id
INVALID_GROUP_NAME = (status.HTTP_400_BAD_REQUEST, 'E305', 'Empty message')  # Group with given name does not exists
USER_ALREADY_EXISTS = (status.HTTP_400_BAD_REQUEST, 'E306', 'Empty message')  # Duplication on username field (and email?)
GROUP_ALREADY_EXISTS = (status.HTTP_400_BAD_REQUEST, 'E307', 'Empty message')  # Duplication on (name, licence_id) pair
GROUP_DOES_NOT_EXIST = (status.HTTP_404_NOT_FOUND, 'E308', 'Empty message')


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
    error = (status.HTTP_400_BAD_REQUEST, 'E310', 'Empty message')


def custom_exception_handler(exc, context):
    # from exception_handler func
    if isinstance(exc, Http404):
        exc = PageNotFound()
    elif isinstance(exc, django_exceptions.PermissionDenied):
        exc = PermissionDenied()
    elif isinstance(exc, exceptions.NotAuthenticated):
        exc = Unauthorized()
    elif isinstance(exc, exceptions.ValidationError):
        # TODO validation errors handling
        # context['view'] - processing view
        exc = ValidationError()

    if isinstance(exc, exceptions.APIException):
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
