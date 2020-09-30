import pytest
import falcon

from user_service.utils import BaseResource, BaseMapper, BaseTO
from user_service.utils.validators import get_type_validator

@pytest.fixture()
def resources():
    class TO(BaseTO):
        def __init__(self, some_str_param=None):
            self.some_str_param = some_str_param

        def as_dict(self):
            return {'some_str_param': self.some_str_param}

        def as_json(self):
            return {'some_str_param': self.some_str_param}

    class Mapper(BaseMapper):
        validators = {
            'some_str_param': [get_type_validator(str)]
        }
        to_class = TO

    class Resource(BaseResource):
        def __init__(self):
            super().__init__()

        mapper = Mapper()

    yield {
        'Resource': Resource,
        'TO': TO,
        'Mapper': Mapper
    }


class TestBaseResource:

    def test_get_mapper(self, resources):
        Mapper = resources['Mapper']
        Resource = resources['Resource']
        res = Resource()
        mapper = res.get_mapper()
        assert type(mapper) == Mapper

    def test_map_with_error_success(self, resources):
        TO = resources['TO']
        Resource = resources['Resource']
        res = Resource()
        input = {
            'some_str_param': 'some_str'
        }
        try:
            to = res.map_with_error(input)
            assert isinstance(to, TO)
            assert to.some_str_param == 'some_str'
        except Exception:
            assert False

    def test_map_with_error_invalid_input_fail(self, resources):
        Resource = resources['Resource']
        res = Resource()
        input = {
            'some_str_param': 10
        }
        try:
            res.map_with_error(input)
            assert False
        except falcon.HTTPBadRequest:
            assert True

    def test_map_with_error_missing_input_fail(self, resources):
        Resource = resources['Resource']
        res = Resource()
        input = {
            'wrong_param_name': 10
        }
        try:
            res.map_with_error(input)
            assert False
        except falcon.HTTPBadRequest:
            assert True
