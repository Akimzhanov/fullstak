"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods
from datetime import timedelta
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "corsheaders",

    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt',
    'django_filters',

    'apps.account',
    'apps.order',
    'apps.smart',
    'chat',
    
    

    

    
]

#

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'middleware.CheckTime',
]

ROOT_URLCONF = 'config.urls'

CORS_ALLOWED_ORIGINS = False


CORS_ALLOWED_ORIGINS = [
    "http://read.only.com",
    "http://204.236.250.233",
    "http://localhost:3000",

]

CSRF_TRUSTED_ORIGINS = [
    "http://change.allowed.com",

]


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3000",
    "http://localhost:3030",
    "http://204.236.250.233",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "delete",
    "post",
    'get',
]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PORT': config('DB_PORT'),
        'HOST': config('DB_HOST'),
        'PASSWORD': config('DB_PASSWORD')
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='ru')

TIME_ZONE = config('TZ', default='UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_DIRS = [
    os.path.join(BASE_DIR, 'config/static'),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKENDS = 'django.core.mail.backends.smtp.EmailBackend' # класс отвечающий за отправку писем
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # почта с которой отправляются письма
EMAIL_PORT = config('EMAIL_PORT', default=587)
EMAIL_HOST = config('EMAIL_HOST') # какой хост используется для отправки писем
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD') # пароль от почты
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool) # вид соединения для отправки писем

AUTH_USER_MODEL = 'account.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    #  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #  'PAGE_SIZE':4,
    #  'SEARCH_PARAM': 'q'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'username',
    'AUTH_HEADER_TYPES': ('Bearer', 'Token'),
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'caches/',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{module} {asctime} {levelname} {filename} {message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            "class": "logging.FileHandler",
            "formatter": "console",
            'filename': 'information.log',
        },

    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },

    },
}