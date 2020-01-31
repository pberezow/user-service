import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_set_password(setup_db, login_session):
    payload = {
        'old_password': 'admin123',
        'new_password': 'admin1234'
    }
    r = login_session.put(url + '/password', json=payload)
    assert r.status_code == HTTPStatus.OK

    r = requests.post(url + '/login', json={'username': 'admin', 'password': 'admin1234'})
    assert r.status_code == HTTPStatus.OK


def test_user_set_password_wrong(setup_db, login_session):
    payload = {
        'old_password': 'wrong_admin123',
        'new_password': 'admin1234'
    }
    r = login_session.put(url + '/password', json=payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST

    r = requests.post(url + '/login', json={'username': 'admin', 'password': 'admin123'})
    assert r.status_code == HTTPStatus.OK


def test_user_set_password_bad_payload(setup_db, login_session):
    payload = {
        'old_password': 'admin123',
        'new_password': 'admin1234',
        'some_data': 'some_data'
    }
    r = login_session.put(url + '/password', json=payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST

    r = requests.post(url + '/login', json={'username': 'admin', 'password': 'admin123'})
    assert r.status_code == HTTPStatus.OK
