import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user, create_non_admin_user_and_login


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_details_delete_new_user(setup_db, login_session, create_non_admin_user_and_login):
    r = login_session.delete(url + '/2')
    assert r.status_code == HTTPStatus.NO_CONTENT

    r = login_session.get(url + '/2')
    assert r.status_code == HTTPStatus.NOT_FOUND


def test_user_delete_self(setup_db, login_session):
    r = login_session.delete(url + '/1')
    assert r.status_code == HTTPStatus.FORBIDDEN

    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', None) is not None


def test_user_delete_admin_by_non_admin(setup_db, login_session, create_non_admin_user_and_login):
    r = login_session.delete(url + '/1')
    assert r.status_code == HTTPStatus.FORBIDDEN

    r = login_session.get(url + '/1')
    assert r.status_code == HTTPStatus.FOUND
    assert r.json().get('user', None) is not None


def test_user_admin_delete_other_org_user(setup_db, create_another_user, login_session):
    r = login_session.delete(url + '/2')
    assert r.status_code == HTTPStatus.NOT_FOUND

    r = login_session.get(url + '/2')
    assert r.status_code == HTTPStatus.NOT_FOUND
