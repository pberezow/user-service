import bcrypt
import jwt
from typing import List, Dict, Optional, Any
from datetime import datetime as dt
from user_service.models.user import UserTO
from user_service.models.exceptions import ValidationException
from user_service.repository.user_repository import UserRepository
from user_service.repository.exceptions import DatabaseException, UserDoesNotExist


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, licence_id: int, username: str, password: str, is_admin: bool, first_name: str,
                    last_name: str, email: str, phone_number: str, address: str, position: str) -> UserTO:
        """
        Creates new user.
        Returns UserTO or raises ValidationException
        """
        hash_password = self._hash_password(password)
        user_to = UserTO(licence_id=licence_id,
                         username=username,
                         password=hash_password,
                         is_admin=is_admin,
                         first_name=first_name,
                         last_name=last_name,
                         email=email,
                         phone_number=phone_number,
                         address=address,
                         position=position,
                         is_active=True,
                         date_joined=dt.now(),
                         last_login=None
                         )
        try:
            user_to.validate(skip_none_values=True)
            user_to = self._user_repository.insert_user(user_to)
        except DatabaseException or ValidationException as err:
            # TODO - add falcon's errors
            raise err

        return user_to

    def get_users_for_licence(self, licence_id: int) -> List[UserTO]:
        """
        Get users with matching licence_id.
        Returns list of users TO witch corresponding licence_id.
        """
        users = self._user_repository.get_users_by_licence_id(licence_id)
        return users

    def get_user(self, licence_id: int, username: str) -> UserTO:
        """
        Get user with matching licence_id and username.
        Returns user TO or raises Exception
        """
        try:
            user_to = self._user_repository.get_user_by_username(username, licence_id)
        except DatabaseException as err:
            raise err

        return user_to

    def set_user_data(self):

        pass

    def remove_user(self, licence_id: int, username: str) -> UserTO:
        """
        Delete user.
        Returns TO for removed user.
        """
        try:
            user_to = self._user_repository.delete_user_by_username(username, licence_id)
        except DatabaseException as err:
            raise err

        return user_to

    def restore_user(self, licence_id: int, username: str) -> UserTO:
        """
        Restore deleted user.
        Returns TO for restored user.
        """
        try:
            user_to = self._user_repository.restore_user_by_username(username, licence_id)
        except DatabaseException as err:
            raise err

        return user_to

    def set_user_groups(self):
        pass

    def set_users_avatar(self):
        pass
