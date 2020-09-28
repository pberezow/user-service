import pytest
import random
from falcon import testing

from user_service.app import UserApplication
from user_service.settings import settings_dict as config


def get_falcon_client():
    return testing.TestClient(UserApplication(config))


def _get_client_with_unique_db():
    indices = [0]

    def func():
        indices.append(indices[-1] + 1)
        config['db']['dbname'] = f'test_db{indices[-1]}'
        print(indices[-1])
        return testing.TestClient(UserApplication(config, init_db=True))

    return func


get_client_with_unique_db = _get_client_with_unique_db()
