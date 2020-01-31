import pytest
import requests
from http import HTTPStatus

from server import db
from server.config import DEFAULT_IP
from server.models.entity import User
from server.utils import hash_password


USERS_IP = 'http://' + DEFAULT_IP + '/api/v1/users'


@pytest.fixture
def setup_db():
    db.drop_all()
    db.create_all()
    new_user_payload = {
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "licence_id": 1,
        "email": "admin@admin.pl",
        "is_admin": True,
        "position": "Admin"
    }
    new_user = User(**new_user_payload)
    db.session.add(new_user)
    db.session.commit()
    yield


@pytest.fixture
def login_session():
    url = USERS_IP + '/login'
    session = requests.Session()
    login_payload = {
        'username': 'admin',
        'password': 'admin123'
    }
    r = session.post(url, json=login_payload)
    if r.status_code != HTTPStatus.OK:
        raise Exception('Error in login_session fixture!')
    yield session


@pytest.fixture
def create_another_user():
    new_user_payload = {
        "username": "qweqweqwe",
        "password_hash": hash_password("qweqwe123"),
        "licence_id": 2,
        "email": "admin1@admin1.pl",
        "is_admin": True
    }
    new_user = User(**new_user_payload)
    db.session.add(new_user)
    db.session.commit()
    yield


@pytest.fixture
def create_non_admin_user_and_login():
    new_user_payload = {
        "username": "test",
        "password_hash": hash_password("test123"),
        "licence_id": 1,
        "email": "admin1@admin1.pl",
        "is_admin": False,
        "position": "NonAdmin"
    }
    new_user = User(**new_user_payload)
    db.session.add(new_user)
    db.session.commit()
    session = requests.Session()
    r = session.post(USERS_IP + '/login', json={'username': 'test', 'password': 'test123'})
    if r.status_code != HTTPStatus.OK:
        raise Exception('Error in login_session fixture!')
    yield session