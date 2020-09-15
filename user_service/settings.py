"""
Django settings for user_service project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta
from .utils import read_rsa_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '94p8wn0=o=dx02e7()f=ny@7kna-7_ynmf+5mo)hdq&=!(mjnu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = True

ALLOWED_HOSTS = ['*']  # ['localhost', '127.0.0.1', '[::1]']  # ['*']

AUTH_USER_MODEL = 'user.User'


# Admins for initadmin command
# ADMINS correct format - (username, password, email) - TODO move to env vars
ADMINS_DATA = [
    ('pberezow', 'admin123', 'pitusx357@gmail.com'),
    ('wzaniewski', 'admin123', 'zaniewski.wojciech97@gmail.com'),
    ('swrobel', 'admin123', 'szywro5@gmail.com'),
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # Django Rest Framework
    'drf_yasg',  # swagger generator

    'group',
    'user',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware for CORS
    'user_service.middleware.cross_origin_middleware',
]


# Config for cross_origin_middleware
ACCESS_CONTROL_ALLOW_ORIGIN = None  # Set header's value to request's Origin header value
ACCESS_CONTROL_ALLOW_HEADERS = ['Origin', 'Content-Type', 'Accept', 'Authorization', 'X-Requested-With', 'X-HTTP-Method-Override']


# DRF config
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'user_service.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


# JWT config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,

    'ALGORITHM': 'RS256',
    'SIGNING_KEY': read_rsa_key(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'keys', 'key')),
    'VERIFYING_KEY': read_rsa_key(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'keys', 'key.pub')),
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.SlidingToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


ROOT_URLCONF = 'user_service.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'user_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB_NAME', 'user_db'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 0,  # (None,  # UNLIMITED) https://github.com/benoitc/gunicorn/issues/996
        'TEST': {
            'NAME': 'user_test_db',
        }
    }
}


# Eureka config - moved to sidecar
EUREKA = {
    'HOST': 'http://eureka:8081/eureka/',
    'DOCKER_PORT': os.environ.get('DOCKER_PORT', '8000'),
    'CONTAINER_ID': os.environ.get('CONTAINER_ID', 'localhost')
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


# Email backend settings
# TODO - move to env
# mail - sili20.test@gmail.com/sili123asd

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # testing

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sili20.test@gmail.com'
EMAIL_HOST_PASSWORD = 'sili123asd'
EMAIL_PORT = 465  # 587  # 465
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = None

from time import sleep
def ready():
    from py_eureka_client import eureka_client
    from user_service.settings import EUREKA

    print(EUREKA['CONTAINER_ID'])
    eureka_up = False
    while not eureka_up:
        try:
            eureka_client.init(
                eureka_server=EUREKA['HOST'],
                app_name='user-service',
                instance_port=int(EUREKA['DOCKER_PORT']),
                instance_host=EUREKA['CONTAINER_ID']
            )
            eureka_up = True
            print('Connected to eureka.')
        except Exception as e:
            print('Connecting to eureka...')
            sleep(2.0)
ready()
