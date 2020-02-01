import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users/permissions'


def test_group_get_all_success(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    payload['name'] = 'new_group2'
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    r = login_session.get(url)
    assert r.status_code == HTTPStatus.OK
    assert len(r.json().get('groups', [])) == 2


def test_group_get_all_when_more_than_one_licence(setup_db, login_session, create_another_user):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    session = requests.Session()
    session.post('http://' + DEFAULT_IP + '/api/v1/users/login',
                 json={'username': 'qweqweqwe', 'password': 'qweqwe123'})

    payload['name'] = 'new_group2'
    r = session.post(url+'/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group!')

    r = login_session.get(url)
    assert r.status_code == HTTPStatus.OK
    assert len(r.json().get('groups', [])) == 1
