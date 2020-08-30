

class UserService:
    def __init__(self, db):
        self._db = db

    def create_user(self, licence_id, username, password, is_admin, first_name, last_name, email,
                    phone_number, address, position):
        pass