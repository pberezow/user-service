import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_set_groups_success(setup_db, login_session):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url + '/permissions/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group')

    r = login_session.put(url + '/1/permissions', json=['new_group'])
    assert r.status_code == HTTPStatus.OK
    assert len(r.json().get('groups', [])) == 1
    assert r.json().get('groups', [])[0].get('name', None) == 'new_group'


def test_user_set_group_non_admin(setup_db, login_session, create_non_admin_user_and_login):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url + '/permissions/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group')

    r = create_non_admin_user_and_login.put(url + '/1/permissions', json=['new_group'])
    assert r.status_code == HTTPStatus.FORBIDDEN


def test_user_set_group_other_licence(setup_db, login_session, create_another_user):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url + '/permissions/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group')

    session = requests.Session()
    session.post('http://' + DEFAULT_IP + '/api/v1/users/login',
                 json={'username': 'qweqweqwe', 'password': 'qweqwe123'})

    r = session.put(url + '/1/permissions', json=['new_group'])
    assert r.status_code == HTTPStatus.BAD_REQUEST


def test_user_set_group_other_licence2(setup_db, login_session, create_another_user):
    payload = {
        'name': 'new_group'
    }
    r = login_session.post(url + '/permissions/add', json=payload)
    if r.status_code != HTTPStatus.CREATED:
        raise Exception('Error while creating group')

    r = login_session.put(url + '/2/permissions', json=['new_group'])
    assert r.status_code == HTTPStatus.BAD_REQUEST

# TODO
