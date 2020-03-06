from django.apps import AppConfig
from time import sleep


class UserConfig(AppConfig):
    name = 'user'

    # def ready(self):
    #     from py_eureka_client import eureka_client
    #     from user_service.settings import EUREKA
    #
    #     eureka_up = False
    #     while not eureka_up:
    #         try:
    #             eureka_client.init(
    #                 eureka_server=EUREKA['HOST'],
    #                 app_name='user-service',
    #                 instance_port=int(EUREKA['DOCKER_PORT'])
    #             )
    #             eureka_up = True
    #         except Exception as e:
    #             sleep(2.0)
