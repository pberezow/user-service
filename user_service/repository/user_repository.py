from datetime import datetime as dt
from user_service.models.user import UserTO


class UserRepository:
    INSERT_USER_QUERY = """
        INSERT INTO users (licence_id, username, password, email, is_admin, first_name, last_name, phone_number,
        address, position, last_login, date_joined, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    DELETE_USER_QUERY = """
        UPDATE users SET is_active = FALSE WHERE id = ?;
    """
    GET_USER_BY_ID_QUERY = """
        SELECT * FROM users WHERE id = ?;
    """
    GET_USERS_BY_LICENCE_ID_QUERY = """
        SELECT * FROM users WHERE licence_id = ? {};
    """
    UPDATE_USER_BY_ID_QUERY = """
        UPDATE users SET {} WHERE id = ?;
    """
    GET_USERS_FOR_GROUP_QUERY = """
        SELECT users.* FROM users 
            JOIN users_groups ON users.id = users_groups.user_id 
            WHERE users.licence_id = ? AND users_groups.group.id = ?
    """

    def __init__(self, db):
        self._db = db

    def insert_user(self, user_to):
        # TODO - execute query
        data = {
            'id': 1,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': True
        }
        user_to = UserTO(
            **data
        )
        return user_to

    def get_user_by_id(self, user_id):
        # TODO
        data = {
            'id': user_id,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name':'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': True
        }
        user_to = UserTO(
            **data
        )
        return user_to

    def delete_user_by_id(self, user_id):
        # TODO
        data = {
            'id': user_id,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': False
        }
        user_to = UserTO(
            **data
        )
        return user_to

    def update_user_by_id(self, user_id, **kwargs):
        # Get updated columns with new values from kwargs and prepare query
        values_to_update = ','.join([f'{key}={value}' for key, value in kwargs.items()])
        query = self.UPDATE_USER_BY_ID_QUERY.format(values_to_update)
        # TODO - execute prepared query and return new user's TO
        data = {
            'id': user_id,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': False,
            **kwargs
        }
        user_to = UserTO(
            **data
        )
        return user_to

    def get_users_by_licence_id(self, licence_id, conditions=None):
        # Get list of conditions and construct query
        conditions_to_include = conditions or []
        conditions_str = ' AND '.join(conditions_to_include)
        query = self.GET_USERS_BY_LICENCE_ID_QUERY.format(conditions_str)
        # TODO - execute prepared query, and return list of user's TO
        data = {
            'id': 1,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': False
        }
        users_to = [UserTO(**data) for _ in range(3)]
        return users_to

    def get_users_for_group(self, group_to):
        # TODO - execute query
        data = {
            'id': 1,
            'licence_id': 1,
            'username': 'user',
            'password': 'password',
            'email': 'asd@asd.asd',
            'is_admin': True,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': '0123456789',
            'address': 'Address 123',
            'position': 'Position',
            'last_login': dt.now(),
            'date_joined': dt.now(),
            'is_active': False
        }
        users_to = [UserTO(**data) for _ in range(3)]
        return users_to
