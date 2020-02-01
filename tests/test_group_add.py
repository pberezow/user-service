import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users/permissions/add'


def test_group_add_success(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url, json=payload)
    assert r.status_code == HTTPStatus.CREATED
    assert r.json().get('name', None) == 'new_group'


def test_group_add_non_admin_user(setup_db, create_non_admin_user_and_login):
    payload = {
        'name': 'new_group'
    }
    r = create_non_admin_user_and_login.post(url, json=payload)
    assert r.status_code == HTTPStatus.FORBIDDEN


def test_group_add_existed_name(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url, json=payload)
    r = login_session.post(url, json=payload)
    assert r.status_code == HTTPStatus.FORBIDDEN
    assert r.json().get('name', None) != 'new_group'


def test_group_add_same_name_another_licence(setup_db, login_session, create_another_user):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url, json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    session = requests.Session()
    session.post('http://' + DEFAULT_IP + '/api/v1/users/login',
                 json={'username': 'qweqweqwe', 'password': 'qweqwe123'})
    r = session.post(url, json=payload)

    assert r.status_code == HTTPStatus.CREATED
