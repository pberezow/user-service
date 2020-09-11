from __future__ import annotations
from typing import Dict, List, Set, Optional, Callable, Any, Union
from abc import ABC
from collections.abc import Iterable

from user_service.exceptions.validation import MissingValidators, InvalidAttributeValueException, MissingUserInput
from user_service.utils.base_to import BaseTO


class BaseMapper(ABC):
    """
    Base class used for mapping user's input into transport objects.

    Contains class attribute 'validators' of type Dict[str, Union[List[Callable]], BaseMapper], which specifies
        list of validators (callable objects) or Mapper for each correct user's input key.
        If 'validators' value is instance of BaseMapper, then provided mapper validates input.

    Class attribute to_class describes class (transport object) to which input from mapping functions will be mapped.

    If mapper is used to validate list of objects (dictionaries), then '__init__' argument - 'many' should be set True.
    If mapper should map only some of specified input keys,
        then '__init__' argument - 'included_attributes' should be set of keys to validate/map.
    If you want to customize nested validators pass them through '__init__' kwarg 'nested_validators'
        as dict with key = nested attribute and value = Mapper
        (Mapper must be same type as specified in mapper class definition)
    """
    validators: Dict[str, Union[List[Callable], BaseMapper]]  # Dict with pairs (attribute name, list of validators)
    to_class: type  # Class to which input will be mapped (subclass of BaseTO)

    @classmethod
    def __init_subclass__(cls):
        if not hasattr(cls, 'validators'):
            raise NotImplementedError(f'{cls} - required class attribute `validators` is missing.')
        else:
            if type(cls.validators) is not dict:
                raise ValueError(
                    f'{cls} - wrong type of `validators` attribute (expected dict, got {type(cls.validators)})'
                )
            else:
                for attribute, validators in cls.validators.items():
                    if not(isinstance(validators, Iterable) or isinstance(validators, BaseMapper)):
                        raise ValueError(
                            f'{cls} - wrong type of validator for {attribute}, '
                            f'expected Iterable or subclass of BaseMapper, got {type(validators)}.'
                        )

        if not hasattr(cls, 'to_class'):
            raise NotImplementedError(f'{cls} - required class attribute `to_class` is missing.')
        else:
            if not issubclass(cls.to_class, BaseTO):
                raise ValueError(
                    f'{cls} - wrong type of `to_class` attribute (should be subclass of `BaseTO`).'
                )

    def __init__(self, many: bool = False,
                 included_attributes: Optional[Set[str]] = None,
                 nested_validators: Optional[Dict[str, BaseMapper]] = None):
        self._many = many

        # check if included_attributes is None or subset of validators
        if included_attributes is None:
            self._included_attributes = set(self.validators.keys())
        elif included_attributes.issubset(set(self.validators.keys())):
            self._included_attributes = included_attributes
        else:
            # if attribute not in validators
            raise MissingValidators(included_attributes.difference(self.validators.keys()), None, type(self))

        # swap nested validators
        if nested_validators is not None:
            for attribute, mapper in nested_validators.items():
                try:
                    if type(self.validators[attribute]) == type(mapper):
                        # swap mapper if type matches
                        self.validators[attribute] = mapper
                    else:
                        # TODO - add new exception for wrong nested mapper type
                        raise MissingValidators(attribute, type(mapper), type(self))
                except KeyError as err:
                    raise MissingValidators(attribute, None, type(self)) from err

    def _validate_attribute(self, attribute: str, value: Any):
        validating_functions = self.validators[attribute]

        if isinstance(validating_functions, BaseMapper):
            # if attribute is another transport object validate all input
            validating_functions.validate(value)
        else:
            for validator in validating_functions:
                if not validator(value):
                    raise InvalidAttributeValueException(attribute, value, type(self))

    def validate(self, users_input: Union[List, Dict[str, Any]]):
        """
        Validate against all validators (all from self._attributes_to_validate).
        returns True or raises InvalidAttributeValueException if validation fails. MissingUserInput if no matching
            key in users_input.
        """
        if self._many and isinstance(users_input, list):
            for obj in users_input:
                self._validate(obj)
        elif not self._many and isinstance(users_input, dict):
            self._validate(users_input)
        else:
            raise InvalidAttributeValueException('users_input', users_input, type(self))
        return True

    def _validate(self, input_dict: Dict[str, Any]):
        # TODO - check if there is no extra items in input_dict?

        for attribute in self._included_attributes:
            try:
                value = input_dict[attribute]
            except KeyError as err:
                raise MissingUserInput(attribute, type(self)) from err

            self._validate_attribute(attribute, value)
        return True

    def _validate_subset(self, input_dict: Dict[str, Any], subset_of_attributes: Set[str]):
        # validate only subset of attributes
        if not subset_of_attributes.issubset(self._included_attributes):
            raise MissingValidators(self._included_attributes.difference(subset_of_attributes), None, type(self))

        for attribute in subset_of_attributes:
            try:
                value = input_dict[attribute]
            except KeyError:
                raise MissingUserInput(attribute, type(self))

            self._validate_attribute(attribute, value)
        return True

    def map_to_transport_object(self, users_input: Union[List, Dict[str, Any]],
                                skip_validation: bool = False) -> Union[BaseTO, List[BaseTO]]:
        """
        Validates and maps input ('users_input') into transport object(s) ('self.to_class')
        If skip_validation == True, then only maps input to transport object(s).
            (Don't! Except when being sure about input)
        """
        # Get attributes used in mapping
        if self._many and isinstance(users_input, list):
            if not skip_validation:
                # list because of map's lazy initialization
                list(map(self._validate, users_input))
            return list(map(self._map_to_transport_object, users_input))
        elif not self._many and isinstance(users_input, dict):
            if not skip_validation:
                self._validate(users_input)
            return self._map_to_transport_object(users_input)
        else:
            # Wrong type of users_input
            raise MissingUserInput(None, type(self))

    def _map_to_transport_object(self, input_dict: Dict[str, Any]) -> BaseTO:
        # Prepare TO input - skip validation on nested Mappers, cause they were already validated in self._validate()
        to_kwargs = {
            attribute:
                input_dict[attribute] if not isinstance(self.validators[attribute], BaseMapper)
                else self.validators[attribute].map_to_transport_object(input_dict[attribute], skip_validation=True)
            for attribute in self._included_attributes
        }
        return self.to_class(**to_kwargs)

    def map_partial_to_transport_object(self, users_input: Union[List, Dict[str, Any]],
                                        subset_of_attributes: Set[str],
                                        skip_validation: bool = False) -> Union[BaseTO, List[BaseTO]]:
        """
        Partial mapping + validation (for UPDATE method in CRUD)
        DOES NOT SUPPORT NESTED MAPPERS YET! - TODO

        For nested mapping put subset of arguments in `nested_subsets_of_attributes` dict in format:
            attribute_name: tuple(subset_of_arguments, nested_subset_of_arguments)
            e.g. nested_subsets_of_attributes = {
                                                    'groups': ({'id', 'name'}, None)
        """
        if self._many and isinstance(users_input, list):
            if not skip_validation:
                # list because of map's lazy initialization
                list(map(lambda dct: self._validate_subset(dct, subset_of_attributes), users_input))
            return list(map(lambda dct: self._map_partial_to_transport_object(dct, subset_of_attributes), users_input))
        elif not self._many and isinstance(users_input, dict):
            if not skip_validation:
                self._validate_subset(users_input, subset_of_attributes)
            return self._map_partial_to_transport_object(users_input, subset_of_attributes)
        else:
            # Wrong type of users_input
            raise MissingUserInput(None, type(self))

    def _map_partial_to_transport_object(self, input_dict: Dict[str, Any], subset_of_attributes: Set[str]) -> BaseTO:
        # Prepare TO input - skip validation on nested Mappers, cause they were already validated in self._validate()
        # DOES NOT SUPPORTS NESTED MAPPERS YET
        to_kwargs = {
            attribute:
                input_dict[attribute] if not isinstance(self.validators[attribute], BaseMapper)
                else self.validators[attribute].map_to_transport_object(input_dict[attribute], skip_validation=True)
            for attribute in subset_of_attributes
        }
        return self.to_class(**to_kwargs)
