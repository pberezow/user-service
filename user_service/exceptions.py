from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status

from django.core.exceptions import PermissionDenied
from django.http.response import Http404

"""
Non service-specific codes:
    'E000' - server error
    'E001' - unauthorized
    'E002' - non admin user
    'E003' - Resource not found
    'E004' - Database error
    
    'E005' - Validation error?
"""


class CustomException(Exception):

    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code='E000', error_message=None):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return f'[Error {self.status_code}]    error code: {self.error_code}    message: {self.error_message}'


class DatabaseError(CustomException):
    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code='E004', error_message=None):
        super().__init__(status_code, error_code, error_message)


def custom_exception_handler(exc, context):
    # from exception_handler func
    if isinstance(exc, Http404):
        exc = CustomException(status.HTTP_404_NOT_FOUND, 'E003')
    elif isinstance(exc, PermissionDenied):
        exc = CustomException(status.HTTP_403_FORBIDDEN, 'E002')
    elif isinstance(exc, exceptions.NotAuthenticated):
        exc = CustomException(exc.status_code, 'E001')
    elif isinstance(exc, exceptions.ValidationError):
        # TODO validation errors handling
        # context['view'] - processing view
        exc = CustomException(exc.status_code, 'E005')

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

    if isinstance(exc, CustomException):
        set_rollback()
        return Response(exc.error_code, status=exc.status_code)

    return None
