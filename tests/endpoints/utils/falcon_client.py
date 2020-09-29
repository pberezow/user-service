import pytest
import random
import os
from falcon import testing
from pathlib import Path

from user_service.app import UserApplication
from user_service.settings import settings_dict as config

_KEYS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys')

def get_falcon_client():
    return testing.TestClient(UserApplication(config, use_eureka=False))


def _get_client_with_unique_db():
    indices = [0]
    with open(os.path.join(_KEYS_PATH, 'key')) as f:
        jwt_prv_key = f.read()
    with open(os.path.join(_KEYS_PATH, 'key.pub')) as f:
        jwt_pub_key = f.read()
    with open(os.path.join(_KEYS_PATH, 'jwt_refresh_key')) as f:
        refresh_key = f.read()

    config['jwt']['private_key'] = jwt_prv_key
    config['jwt']['public_key'] = jwt_pub_key
    config['jwt']['refresh_secret'] = refresh_key

    def func():
        indices.append(indices[-1] + 1)
        config['db']['dbname'] = f'test_db{indices[-1]}'
        print(indices[-1])
        return testing.TestClient(UserApplication(config, init_db=True, use_eureka=False))

    return func


get_client_with_unique_db = _get_client_with_unique_db()
