import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session


url = 'http://' + DEFAULT_IP + '/api/v1/users/token/refresh'


def test_refresh_token_success(setup_db, login_session):
    r = login_session.get(url)
    assert r.cookies.get(JWT_COOKIE_NAME, None) is not None
    assert r.status_code == HTTPStatus.OK


def test_refresh_token_unauthorized_user(setup_db):
    r = requests.get(url)
    assert r.cookies.get(JWT_COOKIE_NAME, None) is None
    assert r.status_code == HTTPStatus.UNAUTHORIZED
