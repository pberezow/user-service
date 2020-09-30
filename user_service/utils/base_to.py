from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseTO(ABC):
    """
    Base class for database transport objects.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """
        Returns Dict with all attributes.
        """
        pass

    @abstractmethod
    def as_json(self) -> Dict[str, Any]:
        """
        Return Dict with all attributes, which can be used as input to json.dumps()
        """
        pass
