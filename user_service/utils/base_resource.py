import falcon
from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict, Any

from user_service.utils.base_mapper import BaseMapper
from user_service.exceptions.validation import InvalidAttributeValueException, MissingUserInput


class BaseResource(ABC):
    """
    Base class for falcon's Resources.
    """
    mapper: Optional[BaseMapper] = None

    @abstractmethod
    def __init__(self):
        pass

    def get_mapper(self):
        """
        Returns mapper or raises NotImplementedError if mapper is None.
        """
        if self.mapper is None:
            raise NotImplementedError(f'{self.__class__} - mapper is missing.')
        return self.mapper

    def map_with_error(self, users_input: Union[List, Dict[str, Any]]):
        """
        Maps input into transport object, and raises falcon's HTTP errors if mapping fails.
        """
        try:
            transport_obj = self.get_mapper().map_to_transport_object(users_input)
        except InvalidAttributeValueException as err:
            raise falcon.HTTPBadRequest(description=f'Invalid `{err.attribute}` value.')
        except MissingUserInput as err:
            raise falcon.HTTPBadRequest(description=f'Missing `{err.attribute}` param in request body.')

        return transport_obj
