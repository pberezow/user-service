import pytest

from user_service.utils import BaseMapper, BaseTO
from user_service.utils.validators import get_type_validator
from user_service.exceptions.validation import InvalidAttributeValueException, MissingUserInput


@pytest.fixture()
def define_mappers():

    class NestedTO(BaseTO):
        def __init__(self, some_float_param=None, some_bool_param=None):
            self.some_float_param = some_float_param
            self.some_bool_param = some_bool_param
            super().__init__()

        def as_dict(self):
            return {'some_float_param': self.some_float_param, 'some_bool_param': self.some_bool_param}

        def as_json(self):
            return {'some_float_param': self.some_float_param, 'some_bool_param': self.some_bool_param}

    class NestedMapper(BaseMapper):
        validators = {
            'some_float_param': [get_type_validator(float)],
            'some_bool_param': [get_type_validator(bool)]
        }
        to_class = NestedTO

    class TO(BaseTO):
        def __init__(self, some_int_param=None, some_str_param=None, some_nested_param=None):
            self.some_int_param = some_int_param
            self.some_str_param = some_str_param
            self.some_nested_param = some_nested_param
            super().__init__()

        def as_dict(self):
            return {'some_int_param': self.some_int_param,
                    'some_str_param': self.some_str_param,
                    'some_nested_param': self.some_nested_param.as_dict()}

        def as_json(self):
            return {'some_int_param': self.some_int_param,
                    'some_str_param': self.some_str_param,
                    'some_nested_param': self.some_nested_param.as_json()}

    class Mapper(BaseMapper):
        validators = {
            'some_int_param': [get_type_validator(int)],
            'some_str_param': [get_type_validator(str)],
            'some_nested_param': NestedMapper()
        }
        to_class = TO

    classes = {
        'NestedTO': NestedTO,
        'NestedMapper': NestedMapper,
        'TO': TO,
        'Mapper': Mapper
    }
    yield classes


class TestMapper:

    def test_mappers_definitions_with_missing_attributes(self):
        try:
            class SomeTO(BaseTO):
                pass

            class MapperWithMissingValidators(BaseMapper):
                to_class = SomeTO
            assert False
        except NotImplementedError:
            assert True
        try:
            class MapperWithMissingTOClass(BaseMapper):
                validators = {'some_float_param': [], 'some_bool_param': []}
            assert False
        except NotImplementedError:
            assert True

    def test_mappers_definitions_with_invalid_attributes(self):
        try:
            class WrongTO:
                pass

            class MapperWithWrongTOType(BaseMapper):
                validators = {'some_float_param': [], 'some_bool_param': []}
                to_class = WrongTO
            assert False
        except ValueError:
            assert True
        try:
            class SomeTO(BaseTO):
                pass

            class MapperWithWrongValidatorsType(BaseMapper):
                validators = ['wrong type']
                to_class = SomeTO
            assert False
        except ValueError:
            assert True

    def test_init_mapers(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        Mapper = define_mappers['Mapper']
        try:
            NestedMapper()
            Mapper()
            assert True
        except Exception:
            assert False

    def test_validate_attribute_success(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        try:
            mapper._validate_attribute('some_float_param', 10.0)
            mapper._validate_attribute('some_bool_param', True)
            assert True
        except InvalidAttributeValueException:
            assert False

    def test_validate_attribute_fail(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        try:
            mapper._validate_attribute('some_float_param', 10)
            assert False
        except InvalidAttributeValueException as err:
            assert err.attribute == 'some_float_param'
            assert err.value == 10
            assert err.mapper == type(mapper)
        try:
            mapper._validate_attribute('some_bool_param', 'not_bool')
            assert False
        except InvalidAttributeValueException as err:
            assert err.attribute == 'some_bool_param'
            assert err.value == 'not_bool'
            assert err.mapper == type(mapper)

    def test_validate_attribute_nested_validation(self, define_mappers):
        Mapper = define_mappers['Mapper']
        mapper = Mapper()
        correct_value = {
            'some_float_param': 10.0,
            'some_bool_param': False
        }
        try:
            mapper._validate_attribute('some_nested_param', correct_value)
            assert True
        except InvalidAttributeValueException:
            assert False

    def test_validate_correct_input_success(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        correct_input = {
            'some_float_param': 10.0,
            'some_bool_param': False
        }
        try:
            assert mapper.validate(correct_input) is True
        except InvalidAttributeValueException:
            assert False

    def test_validate_wrong_input_fail(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        wrong_input = {
            'some_float_param': 10,
            'some_bool_param': 'False'
        }
        try:
            assert mapper.validate(wrong_input) is False
        except InvalidAttributeValueException as err:
            assert True
            assert err.attribute == 'some_float_param' or err.attribute == 'some_bool_param'
            assert err.value == 10 or err.value == 'False'

    def test_validate_with_nested_mapper_success(self, define_mappers):
        Mapper = define_mappers['Mapper']
        mapper = Mapper()
        correct_input = {
            'some_int_param': 10,
            'some_str_param': 'value',
            'some_nested_param': {
                'some_float_param': 10.0,
                'some_bool_param': False
            }
        }
        try:
            assert mapper.validate(correct_input) is True
        except InvalidAttributeValueException:
            assert False

    def test_validate_with_only_some_params(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(included_attributes={'some_float_param'})
        input = {
            'some_float_param': 10.0,
            'some_bool_param': 'not_bool'
        }
        try:
            mapper.validate(input)
        except InvalidAttributeValueException:
            assert False

    def test_validate_with_missing_params_fail(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        input = {
            'some_float_param': 10.0,
        }
        try:
            mapper.validate(input)
            assert False
        except MissingUserInput:
            assert True

    def test_validate_with_extra_parameters(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        input = {
            'some_float_param': 10.0,
            'some_bool_param': True,
            'extra_param': True
        }
        try:
            mapper.validate(input)
        except Exception:
            assert False

    def test_validate_nested_mapper_with_nested_validators_init(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        Mapper = define_mappers['Mapper']
        mapper = Mapper(
            included_attributes={'some_int_param', 'some_nested_param'},
            nested_validators={
                'some_nested_param': NestedMapper(included_attributes={'some_bool_param'})
            })
        input = {
            'some_int_param': 10,
            'some_nested_param': {
                'some_bool_param': False
            }
        }
        try:
            mapper.validate(input)
        except Exception:
            assert False

    def test_validate_many_inputs_success(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(many=True)
        inputs = [
            {
                'some_float_param': 10.0,
                'some_bool_param': True
            },
            {
                'some_float_param': 11.5,
                'some_bool_param': False
            }
        ]
        try:
            mapper.validate(inputs)
        except Exception:
            assert False

    def test_validate_many_inputs_empty_list(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(many=True)
        inputs = []
        try:
            mapper.validate(inputs)
        except Exception:
            assert False

    def test_validate_many_inputs_fail(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(many=True)
        inputs = [
            {
                'some_float_param': 10.0,
                'some_bool_param': True
            },
            {
                'some_float_param': 11.5,
                'some_bool_param': 'False'
            }
        ]
        try:
            mapper.validate(inputs)
            assert False
        except InvalidAttributeValueException:
            assert True

    def test_map_to_transport_object_success(self, define_mappers):
        TO = define_mappers['NestedTO']
        mapper = define_mappers['NestedMapper']()
        input = {
            'some_float_param': 10.0,
            'some_bool_param': True
        }
        try:
            to = mapper.map_to_transport_object(input)
            assert isinstance(to, TO)
            assert to.some_float_param == 10.0
            assert to.some_bool_param is True
        except Exception:
            assert False

    def test_map_to_transport_object_some_attributes_success(self, define_mappers):
        TO = define_mappers['NestedTO']
        mapper = define_mappers['NestedMapper'](included_attributes={'some_bool_param'})
        input = {
            'some_float_param': 10.0,
            'some_bool_param': True
        }
        try:
            to = mapper.map_to_transport_object(input)
            assert isinstance(to, TO)
            assert to.some_float_param is None
            assert to.some_bool_param is True
        except Exception:
            assert False

    def test_map_to_transport_object_some_attributes_fail(self, define_mappers):
        TO = define_mappers['NestedTO']
        mapper = define_mappers['NestedMapper'](included_attributes={'some_bool_param'})
        input = {
            'some_float_param': 10.0,
            'some_bool_param': 'True'
        }
        try:
            to = mapper.map_to_transport_object(input)
            assert False
        except InvalidAttributeValueException as err:
            assert err.attribute == 'some_bool_param'
            assert err.value == 'True'

    def test_map_to_transport_object_nested_mapper(self, define_mappers):
        TO = define_mappers['TO']
        NestedTO = define_mappers['NestedTO']
        mapper = define_mappers['Mapper'](included_attributes={'some_int_param', 'some_nested_param'})
        input = {
            'some_int_param': 10,
            'some_nested_param': {
                'some_float_param': 10.0,
                'some_bool_param': True
            }
        }
        try:
            to = mapper.map_to_transport_object(input)
            assert isinstance(to, TO)
            assert isinstance(to.some_nested_param, NestedTO)
            assert to.some_int_param == 10
            assert to.some_nested_param.some_float_param == 10.0
        except Exception:
            assert False

    def test_map_to_transport_object_many_inputs(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(many=True)
        inputs = [
            {
                'some_float_param': 10.0,
                'some_bool_param': True
            },
            {
                'some_float_param': 11.5,
                'some_bool_param': False
            }
        ]
        try:
            to_list = mapper.map_to_transport_object(inputs)
            assert isinstance(to_list, list)
            assert len(to_list) == 2
            assert to_list[0].some_float_param == 10.0
        except Exception:
            assert False

    def test_map_to_transport_object_many_inputs_fail(self, define_mappers):
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper(many=True)
        inputs = [
            {
                'some_float_param': 10.0,
                'some_bool_param': 'True'
            },
            {
                'some_float_param': 11.5,
                'some_bool_param': False
            }
        ]
        try:
            to_list = mapper.map_to_transport_object(inputs)
            assert False
        except InvalidAttributeValueException as err:
            assert err.attribute == 'some_bool_param'
            assert err.value == 'True'
            assert err.mapper == type(mapper)

    def test_map_partial_to_transport_object(self, define_mappers):
        TO = define_mappers['NestedTO']
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        inputs = {
            'some_float_param': 10.0,
            'some_bool_param': True
        }
        try:
            to = mapper.map_partial_to_transport_object(inputs, subset_of_attributes={'some_float_param'})
            assert isinstance(to, TO)
            assert to.some_float_param == 10.0
            assert to.some_bool_param is None
        except Exception:
            assert False

    def test_map_partial_to_transport_object_fail(self, define_mappers):
        TO = define_mappers['NestedTO']
        NestedMapper = define_mappers['NestedMapper']
        mapper = NestedMapper()
        inputs = {
            'some_float_param': 10,
            'some_bool_param': True
        }
        try:
            to = mapper.map_partial_to_transport_object(inputs, subset_of_attributes={'some_float_param'})
            assert False
        except InvalidAttributeValueException:
            assert True
