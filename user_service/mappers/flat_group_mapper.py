from user_service.utils import BaseMapper
from user_service.utils.validators import get_type_validator, get_str_len_validator
from user_service.models import GroupTO


class FlatGroupMapper(BaseMapper):
    """
    Group mapper without nested `users` attribute.
    """
    validators = {
        'id': [get_type_validator(int)],
        'licence_id': [get_type_validator(int)],
        'name': [get_type_validator(str), get_str_len_validator(max_length=30)]
    }
    to_class = GroupTO
