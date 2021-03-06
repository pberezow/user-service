from typing import Dict, Any
from datetime import datetime

from user_service.utils import BaseTO


class UserTO(BaseTO):
    """
    Transport object representing single row in `users` table. Can also contain groups to which user is assigned through
        join table `users_groups`.
    """
    def __init__(self, id=None, licence_id=None, username=None, password=None, email=None, is_admin=None,
                 first_name=None, last_name=None, phone_number=None, address=None, position=None, last_login=None,
                 date_joined=None, is_active=None, groups=None):
        self.id = id
        self.licence_id = licence_id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.position = position
        self.last_login = last_login
        self.date_joined = date_joined
        self.is_active = is_active
        self.groups = groups or []
        super().__init__()

    def __repr__(self):
        return f'User: {self.id}, {self.username}, {self.email} '

    def add_group(self, group_to: BaseTO):
        """
        Adds group to user's transport object.
        """
        self.groups.append(group_to)

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns dict representation of transport object.
        """
        # return UserTO as Dict
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'is_admin': self.is_admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'position': self.position,
            'last_login': self.last_login,
            'date_joined': self.date_joined,
            'is_active': self.is_active,
            'groups': [g.as_dict() for g in self.groups]
        }

    def as_json(self) -> Dict[str, Any]:
        """
        Returns dict representation of transport object with values, that can be used as input in json.dumps().
        """
        # return UserTO as Dict, which can be an input of json.dumps() - no datetime
        return {
            'id': self.id,
            'licence_id': self.licence_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'is_admin': self.is_admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'position': self.position,
            'last_login': datetime.timestamp(self.last_login) if self.last_login else None,
            'date_joined': datetime.timestamp(self.date_joined) if self.date_joined else None,
            'is_active': self.is_active,
            'groups': [g.as_json() for g in self.groups]
        }
