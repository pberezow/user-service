# import os
# import multiprocessing


settings_dict = {
    'db': {
        'drivername': 'postgres',
        'username': 'user123',
        'password': 'user123',
        'host': 'localhost',
        'port': 5432
    },
    'gunicorn': {
        'reload': True,
        'loglevel': 'debug',
        'errorlog': 'gunicorn.error.log',
        'accesslog': 'gunicorn.log',
        'capture_output': True,
        'bind': [
            'localhost:8080'
        ]
    }
}


class Settings:
    def __init__(self, **kwargs):
        # self._init_kwargs = kwargs
        # print(self._init_kwargs)
        for key, value in kwargs.items():
            self.add_value(key.lower(), value)

    def add_value(self, key, value):
        if type(value) == dict:
            s = Settings(**value)
            setattr(self, key, s)
        else:
            setattr(self, key, value)

    def __repr__(self):
        values = ', '.join([f'{k}: {v}' for k, v in self.__dict__.items()])
        # values = ', '.join(map(lambda k, v: f'{k}: {v}', self.__dict__.items()))
        return f'[ Settings: {values} ]'
