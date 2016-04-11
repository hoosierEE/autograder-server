"""
Django settings for autograder project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json

from django.utils.crypto import get_random_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'filesystem/')

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_secrets(overwrite_prompt=True):
    """
    Generates an app secret key and a database password and writes
    them to a json file.
    """
    secrets_file = os.path.join(SETTINGS_DIR, 'secrets.json')
    if os.path.exists(secrets_file) and overwrite_prompt:
        choice = input(
            'Secrets file already exists. Overwrite? [y/N]'
        ).strip().lower()
        if choice != "y":
            print('Exiting')
            raise SystemExit()

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secrets = {
        'secret_key': get_random_string(50, chars),
        'db_password': get_random_string(50, chars)
    }

    with open(secrets_file, 'w') as f:
        json.dump(secrets, f)


# SECURITY WARNING: keep the secret key used in production secret!
_secrets_filename = os.path.join(SETTINGS_DIR, 'secrets.json')
if not os.path.exists(_secrets_filename):
    generate_secrets(overwrite_prompt=False)

SECRET_KEY = ''
with open(_secrets_filename) as f:
    secrets = json.load(f)
    SECRET_KEY = secrets.pop('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# A list of domain names that users are allowed to authenitcate from.
GOOGLE_IDENTITY_TOOLKIT_APPS_DOMAIN_NAMES = ['umich.edu']
GOOGLE_IDENTITY_TOOLKIT_CONFIG_FILE = os.path.join(
    SETTINGS_DIR, 'gitkit-server-config.json')


LOGIN_URL = '/callback/?mode=select'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'polymorphic',

    'autograder.core',
    'autograder.utilities',
    'autograder.security',
    'autograder.rest_api',
    'autograder.web_interface',

    # Dummy testing models
    'autograder.core.tests.test_models',
    'autograder.core.tests.test_models.test_autograder_test_case',
    'autograder.core.tests.test_models.test_student_test_suite',
]

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'autograder.security.authentication.google_identity_toolkit_session_middleware.GoogleIdentityToolkitSessionMiddleware',

    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'autograder.urls'

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

WSGI_APPLICATION = 'autograder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'autograder_test_db',
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
