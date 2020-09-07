from typing import List, Optional

from user_service.models.user import UserTO
from user_service.repository.user_repository import UserRepository
from user_service.exceptions.database import DatabaseException, UserDoesNotExist
from user_service.utils.password_utils import hash_password


class UserCRUDService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, user_to: UserTO) -> UserTO:
        """
        Creates new user.
        Returns UserTO or None if does not exist in database.
        """
        hashed_pwd = hash_password(user_to.password)
        user_to.password = hashed_pwd
        try:
            user_to = self._user_repository.insert_user(user_to)
        except DatabaseException as err:
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

    def get_user(self, licence_id: int, username: str) -> Optional[UserTO]:
        """
        Get user with matching licence_id and username.
        Returns user TO or None if user does not exist.
        """
        try:
            user_to = self._user_repository.get_user_by_username(username, licence_id)
        except UserDoesNotExist as err:
            return None

        return user_to

    def set_user_data(self):
        pass

    def remove_user(self, licence_id: int, username: str) -> Optional[UserTO]:
        """
        Delete user.
        Returns TO for removed user or None if user does not exist.
        """
        try:
            user_to = self._user_repository.delete_user_by_username(username, licence_id)
        except UserDoesNotExist as err:
            return None

        return user_to

    def restore_user(self, licence_id: int, username: str) -> Optional[UserTO]:
        """
        Restore deleted user.
        Returns TO for restored user or None if user does not exist.
        """
        try:
            user_to = self._user_repository.restore_user_by_username(username, licence_id)
        except UserDoesNotExist as err:
            return None

        return user_to

    def set_user_groups(self):
        pass

    def set_users_avatar(self):
        pass
