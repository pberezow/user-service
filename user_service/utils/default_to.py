from typing import Dict, Any
from datetime import datetime

from user_service.utils import BaseTO


class DefaultTO(BaseTO):
    """
    For mappers not related with database.
    """

    def __init__(self, **kwargs):
        self._attributes = set()
        for k, v in kwargs.items():
            if type(v) == dict:
                value = DefaultTO(**v)
            else:
                value = v
            setattr(self, k, value)
            self._attributes.add(k)
        super().__init__()

    def as_dict(self) -> Dict[str, Any]:
        dct = {}
        for key in self._attributes:
            value = getattr(self, key)
            if type(value) == DefaultTO:
                dct[key] = value.as_dict()
            else:
                dct[key] = value
        return dct

    def as_json(self) -> Dict[str, Any]:
        dct = {}
        for key in self._attributes:
            value = getattr(self, key)
            if isinstance(value, DefaultTO):
                dct[key] = value.as_dict()
            elif type(value) == datetime:
                dct[key] = datetime.timestamp(value)
            else:
                dct[key] = value
        return dct
