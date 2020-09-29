import os
# import multiprocessing
from datetime import timedelta


settings_dict = {
    # JWT config
    'jwt': {
        'private_key': os.environ.get('RSA_PRIVATE_KEY', None),
        'public_key': os.environ.get('RSA_PUBLIC_KEY', None),
        'algorithm': 'RS256',
        'issuer': '1l0t1wIWqZ046DJ88DAqXTdY8lM0baV2AT6kzUw324rBeKh5x5npW8MMvooP',
        'token_lifetime': timedelta(minutes=60),
        'refresh_secret': os.environ.get('REFRESH_TOKEN_KEY', '-HGAGkev2SlEqrHA77iRD6FCo-R30YInMg6RXURT0O8='),
        'refresh_token_lifetime': timedelta(days=1)
    },
    # APP admins
    'admins': [
        {
            'username': 'pberezowski',
            'password': 'admin123',
            'email': 'piotr.berezowski97@gmail.com',
            'licence_id': 0,
            'is_admin': True
        },
        {
            'username': 'wzaniewski',
            'password': 'admin123',
            'email': 'zaniewski.wojciech97@gmail.com',
            'licence_id': 0,
            'is_admin': True
        },
        {
            'username': 'swrobel',
            'password': 'admin123',
            'email': 'szywro5@gmail.com',
            'licence_id': 0,
            'is_admin': True
        }
    ],
    'db_init_script': './user_service/init_db.sql',
    'reset_password_token_lifetime': timedelta(hours=3),
    # DB config
    'db': {
        'engine': 'postgres',
        'username': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': int(os.environ.get('POSTGRES_PORT', '5432')),
        'dbname': os.environ.get('POSTGRES_DB_NAME', 'user_db'),
    },
    # Eureka config
    'eureka': {
        'host': 'http://eureka:8081/eureka/',
        'docker_port': int(os.environ.get('DOCKER_PORT', '8000')),
        'container_id': os.environ.get('CONTAINER_ID', 'localhost')
    },
    # Gunicorn config
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
