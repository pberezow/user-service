import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_update_success(setup_db, login_session):
    payload = {
        'username': 'admin2',
        'email': 'qwe@qwe.qwe',
        'is_admin': True,
        'phone_number': '123456789',
        'address': 'qwedasasf sd',
        'first_name': 'Asd',
        'last_name': 'Qwe',
        'position': 'Admin'
    }

    r = login_session.put(url + '/1', json=payload)
    assert r.status_code == HTTPStatus.OK
    assert r.json().get('username', None) == 'admin2'

    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', {}).get('username', None) == 'admin2'


def test_user_update_partial(setup_db, login_session):
    payload = {
        'first_name': 'Asd',
        'last_name': 'Qwe',
        'position': 'Admin'
    }

    r = login_session.put(url + '/1', json=payload)
    assert r.status_code == HTTPStatus.OK
    assert r.json().get('position', None) == 'Admin'
    assert r.json().get('username', None) == 'admin'

    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', {}).get('position', None) == 'Admin'
    assert r.json().get('user', {}).get('username', None) == 'admin'


def test_user_update_by_non_admin(setup_db, create_non_admin_user_and_login):
    payload = {
        'position': 'Admin'
    }
    r = create_non_admin_user_and_login.put(url + '/2', json=payload)
    assert r.status_code == HTTPStatus.FORBIDDEN
    assert r.json().get('position', None) != 'Admin'

    r = create_non_admin_user_and_login.get(url + '/2')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', {}).get('position', None) == 'NonAdmin'


def test_user_update_another_licence_user(setup_db, login_session, create_another_user):
    payload = {
        'position': 'Admin'
    }
    r = login_session.put(url + '/2', json=payload)
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json().get('position', None) != 'Admin'


def test_user_update_wrong_payload(setup_db, login_session):
    payload = {
        'first_name': 'Asd',
        'last_name': 'Qwe',
        'position': 'NonAdmin',
        'wrong_key': True
    }

    r = login_session.put(url + '/1', json=payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST
    assert r.json().get('position', None) is None

    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', {}).get('position', None) == 'Admin'
