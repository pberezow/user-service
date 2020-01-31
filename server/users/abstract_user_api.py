class AbstractUserAPI:
    def __init__(self):
        self.version = 'v0'

    @staticmethod
    def login(request):
        raise NotImplementedError()

    @staticmethod
    def logout(request):
        raise NotImplementedError()

    @staticmethod
    def refresh_token(request):
        raise NotImplementedError()

    @staticmethod
    def register(request):
        raise NotImplementedError()

    @staticmethod
    def users_list(request):
        raise NotImplementedError()

    @staticmethod
    def user_details_GET(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def user_details_PUT(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def user_details_DELETE(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def set_user_password(request):
        raise NotImplementedError()

    @staticmethod
    def set_user_avatar(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def set_user_groups(request, user_id):
        raise NotADirectoryError()
