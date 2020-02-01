import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users/permissions'


def test_group_delete_success(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    r = login_session.delete(url+'/new_group')
    assert r.status_code == HTTPStatus.NO_CONTENT


def test_group_delete_non_admin_user(setup_db, login_session, create_non_admin_user_and_login):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    r = create_non_admin_user_and_login.delete(url+'/new_group')
    assert r.status_code == HTTPStatus.FORBIDDEN


def test_group_delete_another_licence(setup_db, login_session, create_another_user):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    session = requests.Session()
    session.post('http://' + DEFAULT_IP + '/api/v1/users/login',
                 json={'username': 'qweqweqwe', 'password': 'qweqwe123'})

    r = session.delete(url+'/new_group')
    assert r.status_code == HTTPStatus.NOT_FOUND
