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


def test_user_list_non_admin_success(setup_db, create_another_user, login_session):
    payload = {
        'username': 'test_user',
        'email': 'asd@asd.asda',
        'password': 'test_user1',
        'is_admin': False
    }
    r = login_session.post(url + '/register', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating test user!')

    ses = requests.Session()
    payload.pop('email')
    payload.pop('is_admin')
    r = ses.post(url + '/login', json=payload)
    if r.cookies.get(JWT_COOKIE_NAME, None) is None:
        raise Exception('Error during test_user login!')

    r = ses.get(url)
    assert len(r.json()['users']) == 2
    forbidden_user_fields = ['licence_id', 'username', 'password_hash', 'address', 'id', 'is_admin']
    for user in r.json()['users']:
        for key in user.keys():
            assert key not in forbidden_user_fields
