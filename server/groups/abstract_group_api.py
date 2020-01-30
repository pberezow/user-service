class AbstractGroupAPI:
    def __init__(self):
        self.version = 'v0'

    @staticmethod
    def add_group(request):
        raise NotImplementedError()

    @staticmethod
    def get_all_groups(request):
        raise NotImplementedError()

    @staticmethod
    def set_group(request, group_name):
        raise NotImplementedError()

    @staticmethod
    def delete_group(request, group_name):
        raise NotImplementedError()
