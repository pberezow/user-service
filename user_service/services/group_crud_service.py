from typing import List, Optional

from user_service.models import GroupTO
from user_service.repository import GroupRepository, UserRepository
from user_service.exceptions.database import DatabaseException, UserDoesNotExist, GroupDoesNotExist


class GroupCRUDService:
    """
    Service providing CRUD functionalities for Group object.
    """
    def __init__(self, group_repository: GroupRepository, user_repository: UserRepository):
        self._group_repository = group_repository
        self._user_repository = user_repository

    def create_group(self, group_to: GroupTO) -> GroupTO:
        """
        Creates new group.
        Returns GroupTO.
        """
        try:
            group_to = self._group_repository.insert_group(group_to)
        except DatabaseException as err:
            # TODO - add falcon's errors
            raise err

        return group_to

    def get_groups_for_licence(self, licence_id: int) -> List[GroupTO]:
        """
        Get groups with matching licence_id.
        Returns list of groups TO witch corresponding licence_id.
        """
        groups = self._group_repository.get_groups_by_licence_id(licence_id)
        return groups

    def get_group(self, licence_id: int, name: str) -> Optional[GroupTO]:
        """
        Get group with matching licence_id and name.
        Returns groupTO or None if group does not exist.
        """
        try:
            group_to = self._group_repository.get_group_by_name(name, licence_id)
            users = self._user_repository.get_users_for_group(group_to.id)
            for user in users:
                group_to.add_user(user)
        except GroupDoesNotExist as err:
            return None

        return group_to

    def set_group_data(self):
        pass

    def remove_group(self, licence_id: int, name: str) -> Optional[GroupTO]:
        """
        Delete group.
        Returns TO for removed group or None if group does not exist.
        """
        try:
            group_to = self._group_repository.delete_group_by_name(name, licence_id)
        except GroupDoesNotExist as err:
            return None

        return group_to

    def set_group_users(self):
        pass

