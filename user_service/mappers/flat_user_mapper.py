from datetime import datetime

from user_service.models import UserTO
from user_service.utils import BaseMapper
from user_service.utils.validators import (get_type_validator, email_validator, phone_number_validator,
                                           get_str_len_validator)


class FlatUserMapper(BaseMapper):
    """
    User mapper without nested `groups` attribute.
    """
    validators = {
        'id': [get_type_validator(int)],
        'licence_id': [get_type_validator(int)],
        'username': [get_type_validator(str), get_str_len_validator(min_length=5, max_length=150)],
        'password': [get_type_validator(str), get_str_len_validator(min_length=8, max_length=128)],
        'email': [get_type_validator(str), email_validator, get_str_len_validator(max_length=254)],
        'is_admin': [get_type_validator(bool)],
        'first_name': [get_type_validator(str), get_str_len_validator(max_length=30)],
        'last_name': [get_type_validator(str), get_str_len_validator(max_length=150)],
        'phone_number': [get_type_validator(str), get_str_len_validator(max_length=12),
                         phone_number_validator],
        'address': [get_type_validator(str), get_str_len_validator(max_length=100)],
        'position': [get_type_validator(str), get_str_len_validator(max_length=30)],
        'last_login': [get_type_validator(datetime, type(None))],
        'date_joined': [get_type_validator(datetime)],
        'is_active': [get_type_validator(bool)]
    }
    to_class = UserTO
