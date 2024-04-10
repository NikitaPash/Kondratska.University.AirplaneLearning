"""
Django settings for AirplaneLearning project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import sys
import urllib
from pathlib import Path

import environ
from allauth.account.middleware import AccountMiddleware
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv('.env')
secret_key = os.getenv('secret_key')
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["airplanelearning.azurewebsites.net", "localhost", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = ['https://airplanelearning.azurewebsites.net']

LOGIN_REDIRECT_URL = 'setup/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    "whitenoise.runserver_nostatic",
    "registration_handle.apps.RegistrationHandleConfig",
    "modules.apps.ModulesConfig",
    'profile_page.apps.ProfilePageConfig',
    'drf_yasg',
    'fontawesomefree',
    "discussion_forums.apps.DiscussionForumsConfig"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny'
    )
}

SOCIALACCOUNT_LOGIN_ON_GET = True

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': "92021185036-ija2gcsktesrejq05st3mrst2p8vn6p8.apps.googleusercontent.com",
            'secret': os.environ.get('secret'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTHENTICATION_METHOD = 'GOOGLE'

ROOT_URLCONF = 'ALPP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ALPP.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

load_dotenv('.env')
db_password: str = os.getenv('db_password')

environ.Env.DB_SCHEMES['mssql'] = 'mssql'
env = environ.Env(DEBUG=(bool, False))
DEFAULT_DATABASE_URL = (f"mssql://gearbeagel:{db_password}@alpp-db-server.database.windows.net/alpp-db"
                        f"?driver=ODBC+Driver+17+for+SQL+Server")

DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URL)
os.environ['DJANGO_DATABASE_URL'] = DATABASE_URL.format(**os.environ)

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': env.db('DJANGO_DATABASE_URL', default=DEFAULT_DATABASE_URL)
    }

MEDIA_URL = 'uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_HOST = os.environ.get("DJANGO_STATIC_HOST", "")
STATIC_URL = STATIC_HOST + "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

storage_key: str = os.getenv('storage_key')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        'BACKEND': 'storages.backends.azure_storage.AzureStorage',
        'AZURE_ACCOUNT_NAME': 'alppstorageaccount',
        'AZURE_ACCOUNT_KEY': storage_key,
        'AZURE_CONTAINER': 'pfpcontainer',
    }
}

AZURE_ACCOUNT_NAME = 'alppstorageaccount'
AZURE_ACCOUNT_KEY = storage_key
AZURE_CONTAINER = 'pfpcontainer'


welcome_email_password: str = os.getenv('welcome_email_password')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mnoanyesmai@gmail.com'
EMAIL_HOST_PASSWORD = welcome_email_password
EMAIL_USE_TLS = True
