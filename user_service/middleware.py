"""
Middleware which adds 'Access-Control-Allow-Origin' header to every response
"""
from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)


def cross_origin_middleware(get_response):
    # one-time configuration and initialization
    def empty_middleware(request):
        return get_response(request)

    origin = get('ACCESS_CONTROL_ALLOW_ORIGIN', None)
    headers = get('ACCESS_CONTROL_ALLOW_HEADERS', None)

    if not origin or not headers:
        print('>>> Cross Origin middleware config is missing!')
        return empty_middleware

    if not type(headers) == list or type(headers) == set:
        print('>>> type of ACCESS_CONTROL_ALLOW_HEADERS have to be list or set!')
        return empty_middleware

    for header in headers:
        if not type(header) == str:
            print('>>> type of all ACCESS_CONTROL_ALLOW_HEADERS elements have to be str!')
            return empty_middleware

    if not type(origin) == str:
        print('>>> type of ACCESS_CONTROL_ALLOW_ORIGIN have to be str!')
        return empty_middleware

    def middleware(request):
        # before request being handle

        response = get_response(request)
        response['Access-Control-Allow-Origin'] = settings.ACCESS_CONTROL_ALLOW_ORIGIN
        response['Access-Control-Allow-Headers'] = ', '.join(settings.ACCESS_CONTROL_ALLOW_HEADERS)

        return response

    return middleware
