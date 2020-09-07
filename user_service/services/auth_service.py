import bcrypt
from typing import List, Dict, Optional, Any
from user_service.models.user import UserTO
from user_service.repository.user_repository import UserRepository
from user_service.exceptions.database import DatabaseException, UserDoesNotExist
from user_service.utils.password_utils import is_password_valid


class AuthService:
    def __init__(self, user_repository: UserRepository, jwt_key: str):
        self._user_repository = user_repository
        self._jwt_key = jwt_key

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
