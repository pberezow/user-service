import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user


url = 'http://' + DEFAULT_IP + '/api/v1/users'


def test_user_details_delete_new_user(setup_db, login_session):
    pass


def test_user_delete_self(setup_db, login_session):
    pass


def test_user_delete_admin_by_non_admin(setup_db, login_session):
    pass


def test_user_admin_delete_other_org_user(setup_db, create_another_user, login_session):
    pass
