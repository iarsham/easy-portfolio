import os
import sys
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())
AUTH_USER_MODEL = "users.User"
sys.path.insert(0, os.path.join(BASE_DIR, '../apps'))

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'apps.users.apps.UsersConfig',
    'apps.experience.apps.ExperienceConfig',
    'apps.portfolio.apps.PortfolioConfig',
    'apps.extensions.apps.ExtensionsConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'phonenumber_field',
    'drf_yasg',
    'django_cleanup.apps.CleanupConfig',
]

SITE_ID = 1

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../volumes/static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../volumes/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_ADAPTER = 'apps.extensions.authentication.CustomAllAuthAdaptor'

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.extensions.authentication.ApiKeyAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '25/hour',
        'user': '150/hour'
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.MultiPartRenderer',
    ]
}

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'apps.extensions.authentication.CustomPasswordResetSerializer',
}

REST_AUTH_PW_RESET_USE_SITES_DOMAIN = True

CALLBACK_URL_GITHUB = config('CALLBACK_URL_GOOGLE')
CALLBACK_URL_GOOGLE = config('CALLBACK_URL_GITHUB')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'LOGIN_URL': 'config:login',
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}

CELERY_BROKER_URL = config('BROKER_URL')
CELERY_RESULT_BACKEND = config('BACKEND_URL')
CELERY_TIMEZONE = config('CELERY_TIMEZONE')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
