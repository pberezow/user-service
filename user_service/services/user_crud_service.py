from typing import List, Optional

from user_service.models import UserTO
from user_service.repository import UserRepository, GroupRepository
from user_service.exceptions.database import DatabaseException, UserDoesNotExist
from user_service.utils import hash_password


class UserCRUDService:
    """
    Service providing CRUD functionalities for User object.
    """
    def __init__(self, user_repository: UserRepository, group_repository: GroupRepository):
        self._user_repository = user_repository
        self._group_repository = group_repository

    def create_user(self, user_to: UserTO) -> UserTO:
        """
        Creates new user.
        Returns UserTO.
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
            groups = self._group_repository.get_groups_for_user(user_to.id)
            for group in groups:
                user_to.add_group(group)
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

    def set_user_groups(self, licence_id: int, username: str, groups_names: List[str]) -> Optional[UserTO]:
        """
        Assign user to list of groups
        Returns TO or None if failed to set user groups.
        """
        try:
            self._user_repository.remove_all_user_groups(username, licence_id)
            groups_no = self._user_repository.insert_user_groups_by_group_name(username, licence_id, groups_names)
        except DatabaseException as err:
            return None

        if groups_no == 0:
            return None

        user_to = UserTO(username=username, licence_id=licence_id)
        try:
            groups = self._group_repository.get_groups_for_user(username=username)
            for group in groups:
                user_to.add_group(group)
        except DatabaseException as err:
            # should never occur
            # TODO - logging
            pass

        return user_to

    def set_users_avatar(self):
        pass

    def set_password(self, username: str, raw_password: str) -> bool:
        """
        Set user's password. Returns True if success, otherwise False.
        """
        hashed_pwd = hash_password(raw_password)
        try:
            user_to = self._user_repository.set_users_password(username, hashed_pwd)
            return True
        except UserDoesNotExist as err:
            return False
