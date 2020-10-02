import falcon
from falcon import Request, Response
from typing import Callable, Any, Iterable


class OrPermissionsHook:
    def __init__(self, permissions: Iterable[Callable[[Request, Response, Any, Any], bool]]):
        self._permissions = permissions

    def __call__(self, req: Request, resp: Response, resource, params):
        errors = []
        permitted = False
        for permission in self._permissions:
            try:
                permission(req, resp, resource, params)
                permitted = True
            except falcon.HTTPForbidden as err:
                errors.append(err)

        if not permitted and errors:
            raise errors[0]
