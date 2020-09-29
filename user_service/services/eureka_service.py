import time
from py_eureka_client import eureka_client


class EurekaService:
    """
    Service providing functionalities related to Netflix Eureka service.
    """
    class EurekaConnectionError(Exception):
        """
        Raised when couldn't connect to eureka in `max_connection_tries` tries.
        """
        pass

    def __init__(self, eureka_config: dict):
        self._config = eureka_config
        self.eureka_client = None
        self.max_connection_tries = 10

    def register(self) -> bool:
        """
        Register to eureka service.
        Returns True on success.
        """
        tries = 0
        eureka_up = False
        while not eureka_up:
            try:
                eureka_client.init(
                    eureka_server=self._config['host'],
                    app_name='user-service',
                    instance_port=self._config['docker_port'],
                    instance_host=self._config['container_id']
                )
                eureka_up = True
                print('Connected to eureka.')
            except Exception as err:
                tries += 1
                if tries > self.max_connection_tries:
                    raise self.EurekaConnectionError() from err
                print(f'Connecting to eureka...  ({tries})')
                time.sleep(1.0)
        return True
