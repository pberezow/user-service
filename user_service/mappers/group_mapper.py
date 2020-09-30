from user_service.mappers.flat_user_mapper import FlatUserMapper
from user_service.utils import BaseMapper
from user_service.utils.validators import get_type_validator, get_str_len_validator
from user_service.models import GroupTO


class GroupMapper(BaseMapper):
    """
    Basic Group mapper with nested `users` attribute. Used for user's input validation and mapping to GroupTO obj.
    """
    validators = {
        'id': [get_type_validator(int)],
        'licence_id': [get_type_validator(int)],
        'name': [get_type_validator(str), get_str_len_validator(max_length=30)],
        'users': FlatUserMapper()
    }
    to_class = GroupTO
