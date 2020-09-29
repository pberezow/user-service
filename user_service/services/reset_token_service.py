import _thread
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import uuid4

from user_service.models import UserTO
from user_service.repository import ResetTokenRepository, UserRepository
from user_service.exceptions.database import DatabaseException, TokenDoesNotExist, UserDoesNotExist
from user_service.services import UserCRUDService


class ResetTokenService:
    """
    Service providing functionalities for Password Reset Token.
    """
    def __init__(self, reset_token_repository: ResetTokenRepository, user_repository: UserRepository,
                 user_crud_service: UserCRUDService, token_lifetime: timedelta):
        self._reset_token_repository = reset_token_repository
        self._user_repository = user_repository
        self._user_crud_service = user_crud_service
        self._token_lifetime = token_lifetime
        self.separator = '::'

    def create_token_and_send_email(self, email: str):
        """
        Creates new token for user with email = email (if user exists in db) and then sends email with generated token.
        Starts task on new thread and returns
        """
        _thread.start_new_thread(self._create_token_and_send_email, (email,))

    def reset_password(self, token: str, password: str) -> bool:
        """
        Resets password for user with corresponding token. Returns True on success, otherwise False.
        """
        try:
            user_to = self._reset_token_repository.get_user_for_token(token)
        except TokenDoesNotExist:
            return False
        # set password using UserCRUDService class's method
        return self._user_crud_service.set_password(user_to.username, password)

    def _create_token_and_send_email(self, email: str):
        try:
            user_to = self._user_repository.get_user_by_email(email)
        except UserDoesNotExist:
            # user with this email does not exist
            return

        token = self._create_token(user_to.id)
        if token is None:
            # Cannot create token TODO - log error
            return

        self._send_email(email, token)

    def _send_email(self, email: str, token: str):
        pass

    def _create_token(self, user_id: int) -> Optional[str]:
        """
        Creates reset password token for user with id = user_id.
        Returns token.
        """
        token = self._generate_token()
        try:
            # try update existing record
            success = self._reset_token_repository.set_token_for_user_by_user_id(user_id, token)
            if not success:
                return None
        except TokenDoesNotExist:
            # token does not exist - create new
            try:
                self._reset_token_repository.insert_token(user_id, token)
            except DatabaseException:
                return None
        return token

    def _remove_token(self, user_id: int) -> bool:
        """
        Removes token for user with id = user_id.
        """
        try:
            self._reset_token_repository.delete_token_by_user_id(user_id)
        except TokenDoesNotExist:
            return False
        return True

    def get_user(self, token: str) -> Optional[UserTO]:
        """
        Returns UserTO for reset password token.
        """
        try:
            user_to = self._reset_token_repository.get_user_for_token(token)
        except TokenDoesNotExist:
            return None
        return user_to

    def get_user_id(self, token: str) -> Optional[int]:
        """
        Returns user's id for token.
        """
        try:
            user_id = self._reset_token_repository.get_user_id_for_token(token)
        except TokenDoesNotExist:
            return None
        return user_id

    def _generate_token(self) -> str:
        uuid = str(uuid4())
        time = int((datetime.now() + self._token_lifetime).timestamp())
        token = f'{time}{self.separator}{uuid}'
        return token

    def validate_token(self, token) -> bool:
        try:
            time, uuid = token.split(self.separator)
        except ValueError:
            # wrong token format
            return False

        if datetime.fromtimestamp(int(time)) < datetime.now():
            # expired
            return False
        return True
