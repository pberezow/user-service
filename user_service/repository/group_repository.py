import psycopg2
from typing import List

from user_service.models import GroupTO
from user_service.db import DBManager
from user_service.exceptions.database import GroupDoesNotExist, get_db_exception


class GroupRepository:
    """
    Class used for communication with database. Implements methods related to groups table.
    Each method returns GroupTO, List[GroupTO] or raises DatabaseException
    """

    INSERT_GROUP_QUERY = """
        INSERT INTO groups (licence_id, name) VALUES (%s, %s) RETURNING *;
    """
    DELETE_GROUP_BY_NAME_QUERY = """
        DELETE FROM groups WHERE name = %s AND licence_id = %s RETURNING *;
    """
    GET_GROUP_BY_NAME_QUERY = """
        SELECT * FROM groups WHERE name = %s AND licence_id = %s;
    """
    GET_GROUPS_BY_LICENCE_ID_QUERY = """
        SELECT * FROM groups WHERE licence_id = %s;
    """
    UPDATE_GROUP_BY_NAME_QUERY = """
        UPDATE groups SET {} WHERE name = %s AND licence_id = %s RETURNING *;
    """
    GET_GROUPS_FOR_USER_ID_QUERY = """
        SELECT groups.* FROM groups 
            JOIN users_groups ON groups.id = users_groups.group_id 
            WHERE users_groups.user_id = %s;
    """

    def __init__(self, db: DBManager):
        self._db = db

    @staticmethod
    def _map_record_to_group_to(id, licence_id, name) -> GroupTO:
        """
        Used to map database record (groups table) to GroupTO.
        Arguments order should be same as columns order in groups table.
        """
        return GroupTO(id=id, name=name, licence_id=licence_id)

    def insert_group(self, group_to: GroupTO) -> GroupTO:
        """
        Insert new group into database.
        Return transport object for created group or raise DatabaseException.
        """
        # prepare query params in correct order
        query_params = (group_to.licence_id, group_to.name)
        # execute insert query
        with self._db.session() as cur:
            try:
                cur.execute(self.INSERT_GROUP_QUERY, query_params)
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err

        group_to = self._map_record_to_group_to(*res)
        return group_to

    def get_group_by_name(self, name: str, licence_id: int) -> GroupTO:
        """
        Get group from database.
        Return transport object for group with corresponding name and licence_id or raise GroupDoesNotExist exception.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_GROUP_BY_NAME_QUERY, (name, licence_id))
            res = cur.fetchone()
            if not res:
                raise GroupDoesNotExist()

            group_to = self._map_record_to_group_to(*res)

        return group_to

    def delete_group_by_name(self, name: str, licence_id: int) -> GroupTO:
        """
        Remove group from database and returns deleted group's TO.
        Return transport object for removed group or raise GroupDoesNotExist.
        """
        with self._db.session() as cur:
            try:
                cur.execute(self.DELETE_GROUP_BY_NAME_QUERY, (name, licence_id))
                res = cur.fetchone()
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
        if not res:
            raise GroupDoesNotExist()

        group_to = self._map_record_to_group_to(*res)
        return group_to

    def update_group_by_name(self, name: str, licence_id: int, **kwargs) -> GroupTO:
        """
        Update group's data (kwargs contains pairs (column, new_value)).
        Return transport object for updated group or raise DatabaseException.
        """
        # Get updated columns with new values from kwargs and prepare query
        values_to_update = ','.join([f'{key}={value}' for key, value in kwargs.items()])
        query = self.UPDATE_GROUP_BY_NAME_QUERY.format(values_to_update)
        with self._db.session() as cur:
            try:
                cur.execute(query, (name, licence_id))
                self._db.commit()
            except psycopg2.Error as err:
                self._db.rollback()
                raise get_db_exception(err) from err
            res = cur.fetchone()
        if not res:
            raise GroupDoesNotExist()

        group_to = self._map_record_to_group_to(*res)
        return group_to

    def get_groups_by_licence_id(self, licence_id: int) -> List[GroupTO]:
        """
        Get list of groups with corresponding licence_id from database.
        Return list of transport objects for groups with matching licence_id.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_GROUPS_BY_LICENCE_ID_QUERY, (licence_id,))
            res = cur.fetchall()
        # map results into user transport objects
        groups_to = list(map(lambda group: self._map_record_to_group_to(*group), res))
        return groups_to

    def get_groups_for_user(self, user_id: int) -> List[GroupTO]:
        """
        Get list of groups user belongs to.
        Return list of transport object for groups including user with id = `user_id`.
        """
        with self._db.session() as cur:
            cur.execute(self.GET_GROUPS_FOR_USER_ID_QUERY, (user_id,))
            res = cur.fetchall()
        groups_to = list(map(lambda group: self._map_record_to_group_to(*group), res))
        return groups_to
