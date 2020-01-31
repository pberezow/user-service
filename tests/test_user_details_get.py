import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_details_success(setup_db, login_session):
    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', None) is not None
    assert r.json()['user']['username'] == 'admin'


def test_user_details_unauthorized(setup_db):
    r = requests.get(url + '/1')
    assert r.status_code == HTTPStatus.UNAUTHORIZED
    assert r.json().get('user', None) is None


def test_user_details_different_licence(setup_db, create_another_user, login_session):
    r = login_session.get(url + '/2')
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json().get('user', None) is None


def test_user_details_not_admin_another_details(setup_db, login_session):
    payload = {
        'username': 'test_user',
        'email': 'asd@asd.asda',
        'password': 'test_user1',
        'is_admin': False
    }

    r = login_session.post(url+'/register', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating test user!')

    ses = requests.Session()
    payload.pop('email')
    payload.pop('is_admin')
    r = ses.post(url+'/login', json=payload)
    if r.cookies.get(JWT_COOKIE_NAME, None) is None:
        raise Exception('Error during test_user login!')

    r = ses.get(url + '/1')
    assert r.status_code == HTTPStatus.FORBIDDEN
    assert r.json().get('user', None) is None


def test_user_details_not_admin_self(setup_db, login_session):
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

    r = ses.get(url + '/2')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', None) is not None
