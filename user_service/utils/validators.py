import re
import functools


def get_type_validator(*argument_types):
    return lambda val: functools.reduce(lambda v1, v2: v1 or v2, map(lambda t: type(val) == t, argument_types), False)


"""
String validators
"""


def get_str_len_validator(min_length: int = None, max_length: int = None):
    if min_length is None:
        def min_validator(val): return True
    else:
        def min_validator(val): return len(val) >= min_length

    if max_length is None:
        def max_validator(val): return True
    else:
        def max_validator(val): return len(val) <= max_length

    return lambda val: min_validator(val) and max_validator(val)


EMAIL_REGEX = re.compile(r'[\w\.-]+@([\w-]+\.)+[\w-]{2,4}')
def email_validator(value): return EMAIL_REGEX.fullmatch(value) is not None


PHONE_NUMBER_REGEX = re.compile(r'\+?[0-9]+]')
def phone_number_validator(value): return PHONE_NUMBER_REGEX.fullmatch(value) is not None or not value
