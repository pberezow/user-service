from user_service.utils.base_mapper import BaseMapper
from user_service.services.user_mapper import UserMapper
from user_service.utils.validators import get_type_validator, get_str_len_validator
from user_service.models.group import GroupTO


class GroupMapper(BaseMapper):
    validators = {
        'id': [get_type_validator(int)],
        'licence_id': [get_type_validator(int)],
        'name': [get_type_validator(str), get_str_len_validator(max_length=30)],
        'users': UserMapper()
    }
    to_class = GroupTO
