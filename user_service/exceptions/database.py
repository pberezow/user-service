from typing import Optional
from psycopg2 import Error


class DatabaseException(Exception):
    """Base exception for database errors"""
    def __init__(self, pg_error: Optional[Error] = None):
        self._base_error = pg_error
        if pg_error:
            self.diag = pg_error.diag
        else:
            self.diag = None
        super().__init__()

    def print_diag(self):
        print('PG_Error: ', self._base_error)
        if self._base_error:
            print('column_name: ', self.diag.column_name)
            print('constraint_name: ', self.diag.constraint_name)
            print('context: ', self.diag.context)
            print('datatype_name: ', self.diag.datatype_name)
            print('internal_position: ', self.diag.internal_position)
            print('internal_query: ', self.diag.internal_query)
            print('message_detail: ', self.diag.message_detail)
            print('message_hint: ', self.diag.message_hint)
            print('message_primary: ', self.diag.message_primary)
            print('schema_name: ', self.diag.schema_name)
            print('severity: ', self.diag.severity)
            print('severity_nonlocalized: ', self.diag.severity_nonlocalized)
            print('source_file: ', self.diag.source_file)
            print('source_function: ', self.diag.source_function)
            print('source_line: ', self.diag.source_line)
            print('sqlstate: ', self.diag.sqlstate)
            print('statement_position: ', self.diag.statement_position)
            print('table_name:', self.diag.table_name)


class InvalidAttributeValue(DatabaseException):
    """Raised when attribute type doesn't match db column type or doesn't match constraints on table."""
    def __init__(self, pg_error: Error, attribute: Optional[str] = None, violates_unique: bool = False):
        self.attribute = attribute
        self.violates_unique = violates_unique
        super().__init__(pg_error)


class UserDoesNotExist(DatabaseException):
    """Raised when user does not exist in database."""
    pass


class GroupDoesNotExist(DatabaseException):
    """Raised when group does not exist in database."""
    pass


class TokenDoesNotExist(DatabaseException):
    """Raised when reset_password_token does not exist in database."""
    pass


class UserAlreadyInGroup(DatabaseException):
    """Raised when trying to assign user to group, which already includes him."""
    pass


def get_db_exception(pg_error: Error) -> DatabaseException:
    # Exceptions related to 'users' table
    if pg_error.diag.table_name == 'users':
        if pg_error.diag.constraint_name == 'users_username_key':
            raise InvalidAttributeValue(pg_error, 'username', True)
        pass

    # Exceptions related to 'groups' table
    elif pg_error.diag.table_name == 'groups':
        if pg_error.diag.constraint_name == 'groups_licence_id_name':
            raise InvalidAttributeValue(pg_error, 'name', True)
        pass

    # Exceptions related to 'users_groups' table
    elif pg_error.diag.table_name == 'users_groups':
        if pg_error.diag.constraint_name == 'users_groups_pkey':
            raise UserAlreadyInGroup(pg_error)
        elif pg_error.diag.constraint_name == 'users_groups_group_id_fk_groups_id':
            raise GroupDoesNotExist()
        elif pg_error.diag.constraint_name == 'users_groups_user_id_fk_users_id':
            raise UserDoesNotExist()
        pass

    # All other database-related errors
    return DatabaseException(pg_error)
