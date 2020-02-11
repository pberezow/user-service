import os


def read_rsa_key(filename):
    try:
        with open(filename, 'r') as f:
            key = f.read()
            return key
    except:
        Exception('Error while reading rsa key file - ', filename)


# FLASK APP
FLASK_APP = 'server/__init__.py'
DEFAULT_IP = '0.0.0.0:3000'
DEFAULT_PORT = 3000

# DATABASE
_DB_USER = 'user_service'
_DB_PASSWORD = 'user_service'
_POSTGRES_URL = 'localhost:5432'
_DB_NAME = 'user_service_db'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=_DB_USER, pw=_DB_PASSWORD, url=_POSTGRES_URL, db=_DB_NAME)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.db'

URI_PREFIX = '/api/v1/users'

# RSA KEYS for JWT
_PRIVATE_KEY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'keys', 'key')
PRIVATE_KEY = read_rsa_key(_PRIVATE_KEY_PATH)

_PUBLIC_KEY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'keys', 'key.pub')
PUBLIC_KEY = read_rsa_key(_PUBLIC_KEY_PATH)

JWT_COOKIE_NAME = 'token'

# SALT for password encryption
SALT_PRE = 'A#c.+!Y17asU'  # put this before password string
SALT_POST = 'X$AY67!'  # put this after password string

# EUREKA CONFIG
EUREKA_IP = 'http://localhost:8081/eureka/'
