import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users/permissions'


def test_group_set_data_success(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    payload['name'] = 'new_group2'
    r = login_session.put(url+'/new_group', json=payload)
    print(r.json())
    assert r.status_code == HTTPStatus.OK
    assert r.json().get('name', None) == 'new_group2'


def test_group_set_data_non_admin_user(setup_db, login_session, create_non_admin_user_and_login):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url + '/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    payload['name'] = 'new_group2'
    r = create_non_admin_user_and_login.put(url + '/new_group', json=payload)
    assert r.status_code == HTTPStatus.FORBIDDEN
    assert r.json().get('name', None) is None
