import requests
import pytest
from http import HTTPStatus

from server.config import DEFAULT_IP, JWT_COOKIE_NAME
from .fixtures import setup_db, login_session, create_another_user


url = 'http://' + DEFAULT_IP + '/api/v1/users'

# TODO
