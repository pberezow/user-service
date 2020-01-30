from http import HTTPStatus

from server.groups.abstract_group_api import AbstractGroupAPI
from server.utils import error_message


class GroupAPI(AbstractGroupAPI):
    def __init__(self):
        super().__init__()
        self.version = 'v1'

    @staticmethod
    def add_group(request):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def get_all_groups(request):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def set_group(request, group_name):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def delete_group(request, group_name):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)
