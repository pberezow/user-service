import psycopg2
from typing import List, Optional

from user_service.models import UserTO
from user_service.db import DBManager
from user_service.exceptions.database import UserDoesNotExist, get_db_exception


class UserRepository:
    """
    Class used for communication with database. Implements methods related to users table.
    Each method returns UserTO, List[UserTO] or raises DatabaseException
    """

    INSERT_USER_QUERY = """
        INSERT INTO users (licence_id, username, password, email, is_admin, first_name, last_name, phone_number,
        address, position, last_login, date_joined, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """
    DELETE_USER_BY_USERNAME_QUERY = """
        UPDATE users SET is_active = FALSE WHERE username = %s AND licence_id = %s AND is_active = TRUE RETURNING *;
    """
    HARD_DELETE_USER_BY_USERNAME_QUERY = """
        DELETE FROM users WHERE username = %s AND licence_id = %s RETURNING *;
    """
    RESTORE_USER_BY_USERNAME_QUERY = """
        UPDATE users SET is_active = TRUE WHERE username = %s AND licence_id = %s AND is_active = FALSE RETURNING *;
    """
    GET_USER_BY_USERNAME_QUERY = """
        SELECT * FROM users WHERE username = %s AND licence_id = %s;
    """
    GET_USER_BY_EMAIL_QUERY = """
            SELECT * FROM users WHERE email = %s;
    """
    GET_USER_FOR_AUTHENTICATION_QUERY = """
        SELECT * FROM users WHERE username = %s AND is_active = TRUE;
    """
    GET_USERS_BY_LICENCE_ID_QUERY = """
        SELECT * FROM users WHERE licence_id = %s;
    """
    UPDATE_USER_BY_USERNAME_QUERY = """
        UPDATE users SET {} WHERE username = %s AND licence_id = %s AND is_active = TRUE RETURNING *;
    """
    GET_USERS_FOR_GROUP_ID_QUERY = """
        SELECT users.* FROM users 
            JOIN users_groups ON users.id = users_groups.user_id 
            WHERE users_groups.group_id = %s AND users.is_active = TRUE;
    """
    SET_PASSWORD_QUERY = """
        UPDATE users set password = %s WHERE username = %s AND is_active = TRUE RETURNING *;
    """
    REMOVE_ALL_USER_GROUPS_QUERY = """
        DELETE FROM users_groups 
            WHERE user_id = (SELECT id FROM users WHERE username = %s AND licence_id = %s) RETURNING *;
    """
    INSERT_USER_GROUPS_BY_GROUP_NAME_QUERY = """
        INSERT INTO users_groups (user_id, group_id) SELECT users.id, groups.id FROM users
            JOIN groups ON users.licence_id = groups.licence_id 
            WHERE users.username = %s AND users.licence_id = %s AND groups.name = ANY(%s) RETURNING *;
    """

    def __init__(self, db: DBManager):
        self._db = db

    @staticmethod
    def map_record_to_user_to(id, password, last_login, username, first_name, last_name, email, is_active,
                               date_joined, licence_id, is_admin, phone_number, address, position) -> UserTO:
        """
        Used to map database record (users table) to UserTO.
        Arguments order should be same as columns order in users table.
        """
        return UserTO(id=id, password=password, last_login=last_login, username=username,
                      first_name=first_name, last_name=last_name, email=email, is_active=is_active,
                      date_joined=date_joined, licence_id=licence_id, is_admin=is_admin,
                      phone_number=phone_number, address=address, position=position)

    def insert_user(self, user_to: UserTO) -> UserTO:
        """
        Insert new user into database.
        Return transport object for created user or raise DatabaseException.
        """
        # prepare query params in correct order
        query_params = (user_to.licence_id, user_to.username, user_to.password, user_to.email, user_to.is_admin,
                        user_to.first_name, user_to.last_name, user_to.phone_number, user_to.address, user_to.position,
                        user_to.last_login, user_to.date_joined, user_to.is_active)
        # execute insert query
        with self._db.session() as cur:
            try:
                cur.execute(self.INSERT_USER_QUERY, query_params)
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def get_user_by_username(self, username: str, licence_id: Optional[int], for_auth: bool = False) -> UserTO:
        """
        Get user from database. Set licence_id = None and for_auth = True for querying only with username.
        Return transport object for user with corresponding username and licence_id or raise UserDoesNotExist exception.
        """
        with self._db.session() as cur:
            if for_auth:
                cur.execute(self.GET_USER_FOR_AUTHENTICATION_QUERY, (username,))
            else:
                cur.execute(self.GET_USER_BY_USERNAME_QUERY, (username, licence_id))

            res = cur.fetchone()
            if not res:
                raise UserDoesNotExist()

            user_to = self.map_record_to_user_to(*res)

        return user_to

    def get_user_by_email(self, email: str) -> UserTO:
        """
        Get user from database.
        Return transport object for user with corresponding email or raise UserDoesNotExist exception.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_USER_BY_EMAIL_QUERY, (email,))
            res = cur.fetchone()
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)

        return user_to

    def delete_user_by_username(self, username: str, licence_id: int) -> UserTO:
        """
        Set user inactive (is_active = False).
        Return transport object for updated user or raise Database exception.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.DELETE_USER_BY_USERNAME_QUERY, (username, licence_id))
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def hard_delete_user_by_username(self, username: str, licence_id: int) -> UserTO:
        """
        Hard delete user.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.HARD_DELETE_USER_BY_USERNAME_QUERY, (username, licence_id))
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def restore_user_by_username(self, username: str, licence_id: int) -> UserTO:
        """
        Set user active (is_active = True).
        Return transport object for updated user or raise DatabaseException.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.RESTORE_USER_BY_USERNAME_QUERY, (username, licence_id))
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def update_user_by_username(self, _username: str, _licence_id: int, **kwargs) -> UserTO:
        """
        Update user's data (kwargs contains pairs (column, new_value)).
        Return transport object for updated user or raise DatabaseException.
        """
        # Get updated columns with new values from kwargs and prepare query
        values_to_update = ', '.join([f'{key} = %s' for key in kwargs.keys()])
        query = self.UPDATE_USER_BY_USERNAME_QUERY.format(values_to_update)
        with self._db.session() as cur:
            try:
                cur.execute(query, (*kwargs.values(), _username, _licence_id))
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
            res = cur.fetchone()
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def get_users_by_licence_id(self, licence_id: int) -> List[UserTO]:
        """
        Get list of users with corresponding licence_id from database.
        Return list of transport objects for users with matching licence_id.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_USERS_BY_LICENCE_ID_QUERY, (licence_id,))
            res = cur.fetchall()
        # map results into user transport objects
        users_to = list(map(lambda user: self.map_record_to_user_to(*user), res))
        return users_to

    def get_users_for_group(self, group_id: int) -> List[UserTO]:
        """
        Get list of users assigned to some group (GroupTO) from database.
        Return list of transport object for users assigned to group.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_USERS_FOR_GROUP_ID_QUERY, (group_id,))
            res = cur.fetchall()
        users_to = list(map(lambda user: self.map_record_to_user_to(*user), res))
        return users_to

    def set_users_password(self, username: str, password: str) -> UserTO:
        """
        Set password for user with matching username.
        Returns UserTO or raises UserDoesNotExist.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.SET_PASSWORD_QUERY, (password, username))
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err)
            res = cur.fetchone()
        if not res:
            raise UserDoesNotExist()

        user_to = self.map_record_to_user_to(*res)
        return user_to

    def remove_all_user_groups(self, username: str, licence_id: int) -> int:
        """
        Remove user from all groups he belongs to.
        Returns number of removed assignments between user and group.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.REMOVE_ALL_USER_GROUPS_QUERY, (username, licence_id))
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err)
            res = cur.fetchall()
        return len(res)

    def insert_user_groups_by_group_name(self, username: str, licence_id: int, groups_names: List[str]) -> int:
        """
        Assign user to each group from list of passed group names.
        Returns number of groups user was assigned to.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.INSERT_USER_GROUPS_BY_GROUP_NAME_QUERY, (username, licence_id, groups_names))
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err)
            res = cur.fetchall()
        return len(res)
