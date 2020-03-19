"""
Middleware which adds 'Access-Control-Allow-Origin' header to every response
"""
from django.conf import settings


DEFAULT_ACCESS_CONTROL_ALLOW_ORIGIN = '*'
DEFAULT_ACCESS_CONTROL_ALLOW_HEADERS = '*'
DEFAULT_ACCESS_CONTROL_ALLOW_CREDENTIALS = 'true'
DEFAULT_ACCESS_CONTROL_MAX_AGE = '1728000'


def get(key, default):
    return getattr(settings, key, default)


def cross_origin_middleware(get_response):
    # one-time configuration and initialization
    origin = get('ACCESS_CONTROL_ALLOW_ORIGIN', DEFAULT_ACCESS_CONTROL_ALLOW_ORIGIN)
    headers = get('ACCESS_CONTROL_ALLOW_HEADERS', DEFAULT_ACCESS_CONTROL_ALLOW_HEADERS)
    credentials = get('ACCESS_CONTROL_ALLOW_CREDENTIALS', DEFAULT_ACCESS_CONTROL_ALLOW_CREDENTIALS)
    max_age = get('ACCESS_CONTROL_MAX_AGE', DEFAULT_ACCESS_CONTROL_MAX_AGE)

    if isinstance(headers, list) or isinstance(headers, set):
        try:
            ','.join(headers)
        except Exception as e:
            headers = DEFAULT_ACCESS_CONTROL_ALLOW_HEADERS

    if credentials not in ('true', 'false'):
        credentials = 'true'

    def middleware(request):
        # before request being handle

        response = get_response(request)

        response['Access-Control-Allow-Origin'] = origin or request.headers.get('Origin', DEFAULT_ACCESS_CONTROL_ALLOW_ORIGIN)
        response['Access-Control-Allow-Credentials'] = credentials  # for axios withCredentials option
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = headers or DEFAULT_ACCESS_CONTROL_ALLOW_HEADERS
            response['Access-Control-Max-Age'] = max_age or DEFAULT_ACCESS_CONTROL_MAX_AGE  # for OPTIONS caching

        return response

    return middleware
