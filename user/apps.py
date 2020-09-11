from django.apps import AppConfig
from time import sleep


class UserConfig(AppConfig):
    name = 'user'

    # def ready(self):
    #     from py_eureka_client import eureka_client
    #     from user_service.settings import EUREKA
    #
    #     print('asdasdasdsad')
    #     eureka_up = False
    #     while not eureka_up:
    #         try:
    #             eureka_client.init(
    #                 eureka_server=EUREKA['HOST'],
    #                 app_name='user-service',
    #                 instance_port=int(EUREKA['DOCKER_PORT']),
    #                 instance_host=EUREKA['CONTAINER_ID']
    #             )
    #             eureka_up = True
    #             print('Connected to eureka.')
    #         except Exception as e:
    #             print('Connecting to eureka...')
    #             sleep(2.0)
