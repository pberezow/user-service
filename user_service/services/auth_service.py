from typing import Optional

from user_service.models import UserTO
from user_service.repository import UserRepository
from user_service.exceptions.database import DatabaseException, UserDoesNotExist
from user_service.utils import is_password_valid


class AuthService:
    """
    Service providing authorization functionalities.
    """
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> Optional[UserTO]:
        """
        Authenticate user with matching username and password.
        Returns user's TO if authentication succeed, otherwise returns None
        """
        try:
            user_to = self._user_repository.get_user_by_username(username, licence_id=None, for_auth=True)
        except UserDoesNotExist as err:
            return None

        if is_password_valid(password, user_to.password):
            return user_to
        else:
            return None
