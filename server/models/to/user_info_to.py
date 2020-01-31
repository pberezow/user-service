from .abstract_to import AbstractTO


class UserInfoTO(AbstractTO):
    def __init__(self, user_model):
        super().__init__(user_model)
        self.email = user_model.email
        self.phone_number = user_model.phone_number
        self.first_name = user_model.first_name
        self.last_name = user_model.last_name
        self.position = user_model.position

    def to_dict(self):
        return {
            'email': self.email,
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position
        }
