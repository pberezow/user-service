from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        from py_eureka_client import eureka_client
        from user_service.settings import EUREKA

        eureka_client.init(
            eureka_server=EUREKA['HOST'],
            app_name='user-service',
            instance_port=int(EUREKA['DOCKER_PORT'])
        )
