import psycopg2
from typing import Optional

from user_service.models import UserTO
from user_service.db import DBManager
from user_service.exceptions.database import TokenDoesNotExist, get_db_exception
from user_service.repository.user_repository import UserRepository


class ResetTokenRepository:
    """
    Class used for communication with database. Implements methods related to reset_password_token table.
    """

    INSERT_TOKEN_QUERY = """
        INSERT INTO reset_password_token (user_id, token) VALUES (%s, %s) RETURNING *;
    """
    DELETE_TOKEN_BY_USER_ID_QUERY = """
        DELETE FROM reset_password_token WHERE user_id = %s RETURNING *;
    """
    SET_TOKEN_BY_USER_ID_QUERY = """
        UPDATE reset_password_token SET token = %s WHERE user_id = %s RETURNING *;
    """
    GET_USER_FOR_TOKEN_QUERY = """
        SELECT users.* FROM users 
            JOIN reset_password_token ON users.id = reset_password_token.user_id 
            WHERE reset_password_token.token = %s;
    """
    GET_USER_ID_FOR_TOKEN_QUERY = """
        SELECT user_id FROM reset_password_token WHERE token = %s;
    """
    GET_TOKEN_FOR_USER_ID = """
        SELECT token FROM reset_password_token WHERE user_id = %s;
    """

    def __init__(self, db: DBManager):
        self._db = db

    def insert_token(self, user_id: int, token: str) -> bool:
        """
        Insert new token into database.
        Return True if success or raise DatabaseException.
        """
        # execute insert query
        with self._db.session() as cur:
            try:
                cur.execute(self.INSERT_TOKEN_QUERY, (user_id, token))
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err

        return True

    def delete_token_by_user_id(self, user_id: int) -> bool:
        """
        Remove token assigned to user with specified user_id.
        """
        with self._db.session() as cur:
            cur.execute(self.DELETE_TOKEN_BY_USER_ID_QUERY, (user_id,))
            res = cur.fetchone()
            if not res:
                raise TokenDoesNotExist()

        return True

    def set_token_for_user_by_user_id(self, user_id: int, token: str) -> bool:
        with self._db.session() as cur:
            cur.execute(self.SET_TOKEN_BY_USER_ID_QUERY, (token, user_id))
            res = cur.fetchone()
            if not res:
                raise TokenDoesNotExist()

        return True

    def get_user_for_token(self, token: str) -> UserTO:
        with self._db.session() as cur:
            cur.execute(self.GET_USER_FOR_TOKEN_QUERY, (token,))
            res = cur.fetchone()
            if not res:
                raise TokenDoesNotExist()
            user_to = UserRepository.map_record_to_user_to(*res)

        return user_to

    def get_user_id_for_token(self, token: str) -> int:
        with self._db.session() as cur:
            cur.execute(self.GET_USER_ID_FOR_TOKEN_QUERY, (token,))
            res = cur.fetchone()
            if not res:
                raise TokenDoesNotExist()
            user_id = res[0]

        return user_id

    def get_token_for_user_id(self, user_id: int) -> str:
        with self._db.session() as cur:
            cur.execute(self.GET_TOKEN_FOR_USER_ID, (user_id,))
            res = cur.fetchone()
            if not res:
                raise TokenDoesNotExist()
            token = res[0]

        return token
