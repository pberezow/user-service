from typing import Dict, Tuple, Any
from user_service.utils import BaseTO


class GroupTO(BaseTO):
    def __init__(self, id, licence_id, name, users=None):
        self.id = id
        self.licence_id = licence_id
        self.name = name
        self.users = users or []
        super().__init__()

    def add_user(self, user_to):
        self.users.append(user_to)

    def as_dict(self) -> Dict[str, Any]:
        # return UserTO as Dict
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'name': self.name,
            'users': [u.as_dict() for u in self.users]
        }

    def as_json(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'name': self.name,
            'users': [u.as_json() for u in self.users]
        }
