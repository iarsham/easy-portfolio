from .base import *

INSTALLED_APPS += [
    "corsheaders",
]

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
]

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

CORS_ALLOW_ALL_ORIGINS = True
