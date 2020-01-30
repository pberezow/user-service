import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_list_success(setup_db, create_another_user, login_session):
    r = login_session.get(url)
    assert r.status_code == HTTPStatus.OK
    assert len(r.json()['users']) == 1
    for user in r.json()['users']:
        assert user['licence_id'] == 1


def test_user_list_unauthorized(setup_db, create_another_user):
    r = requests.get(url)
    assert r.json().get('users', None) is None
    assert r.status_code == HTTPStatus.UNAUTHORIZED
