import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session


USERS_IP = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_login_success(setup_db):
    url = USERS_IP + '/login'
    login_payload = {
        'username': 'admin',
        'password': 'admin123'
    }
    r = requests.post(url, json=login_payload)
    assert r.cookies.get(JWT_COOKIE_NAME, None) is not None
    assert r.status_code == HTTPStatus.OK


def test_user_login_wrong_password(setup_db):
    url = USERS_IP + '/login'
    login_payload = {
        'username': 'admin',
        'password': 'admin1234'
    }
    r = requests.post(url, json=login_payload)
    assert r.cookies.get(JWT_COOKIE_NAME, None) is None
    assert r.status_code == HTTPStatus.BAD_REQUEST


def test_user_login_wrong_username(setup_db):
    url = USERS_IP + '/login'
    login_payload = {
        'username': 'admin1',
        'password': 'admin123'
    }
    r = requests.post(url, json=login_payload)
    assert r.cookies.get(JWT_COOKIE_NAME, None) is None
    assert r.status_code == HTTPStatus.BAD_REQUEST


def test_user_register_success(setup_db, login_session):
    url = USERS_IP + '/register'
    payload = {
        'username': 'user1',
        'password': 'user1',
        'email': 'asd@asd.asd',
        'is_admin': False
    }
    r = login_session.post(url, json=payload)
    assert r.status_code == HTTPStatus.CREATED


def test_user_register_by_unauthorized_user(setup_db):
    url = USERS_IP + '/register'
    payload = {
        'username': 'user1',
        'password': 'user1',
        'email': 'asd@asd.asd',
        'is_admin': False
    }
    r = requests.post(url, json=payload)
    assert r.status_code == HTTPStatus.UNAUTHORIZED


def test_user_register_no_email_provided(setup_db, login_session):
    url = USERS_IP + '/register'
    payload = {
        'username': 'user1',
        'password': 'user1',
        'is_admin': False
    }
    r = login_session.post(url, json=payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST
