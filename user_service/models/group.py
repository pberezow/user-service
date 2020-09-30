from typing import Dict, Any

from user_service.utils import BaseTO


class GroupTO(BaseTO):
    """
    Transport object representing single row in `groups` table. Can also contain users assigned to group through
        join table `users_groups`.
    """
    def __init__(self, id=None, licence_id=None, name=None, users=None):
        self.id = id
        self.licence_id = licence_id
        self.name = name
        self.users = users or []
        super().__init__()

    def add_user(self, user_to: BaseTO):
        """
        Adds user to group transport object. `user_to` should be type of `UserTO`.
        """
        self.users.append(user_to)

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns dict representation of transport object.
        """
        # return UserTO as Dict
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'name': self.name,
            'users': [u.as_dict() for u in self.users]
        }

    def as_json(self) -> Dict[str, Any]:
        """
        Returns dict representation of transport object with values, that can be used as input in json.dumps().
        """
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'name': self.name,
            'users': [u.as_json() for u in self.users]
        }
