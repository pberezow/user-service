from server.models.entity.user_model import User
from server.utils import encode_JWT


class UserDetailsTO:
    def __init__(self, user_model):
        self.licence_id     = user_model.licence_id
        self.username       = user_model.username 
        self.email          = user_model.email
        self.is_admin       = user_model.is_admin
        self.phone_number   = user_model.phone_number
        self.address        = user_model.address
        self.first_name     = user_model.first_name
        self.last_name      = user_model.last_name
        self.position       = user_model.position
        self.groups         = None # TODO

    @classmethod
    def from_list(cls, users_list):
        users = []
        for user in users_list:
            users.append(cls(user))
        return users

    def get_jwt(self):
        jwt_payload = {
            'licence_id': self.licence_id,
            'username': self.username,
            'is_admin': self.is_admin,
            'position': self.position,
            'email': self.email
        }
        
        encoded_jwt = encode_JWT(jwt_payload)
        return encoded_jwt

    def to_dict(self):
        return {
            'licence_id': self.licence_id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'phone_number': self.phone_number,
            'address': self.address,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'groups': None # TODO
        }