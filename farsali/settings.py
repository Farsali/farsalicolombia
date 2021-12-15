# coding: utf-8
import os

import django_heroku
import environ
from django import http
from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

# Only for local development and CI, env variables take precedence
env = environ.Env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "lr+ke#n6om%_evagj1-=-piroo%b^x4_ktr+*b8!(57#49%8oe"

MEDIA_URL = "/"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "farsalicol.herokuapp.com",
    "localhost:8000",
    "www.farsalicolombia.com",
    "farsalicolombia.com",
    "polar-tor-89642.herokuapp.com",
    "127.0.0.1",
    "*",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "rangefilter",
    "sorl.thumbnail",
    "storages",
    "farsali.apps",
    "farsali.apps.clientes",
    "farsali.apps.inventario",
    "farsali.apps.ventas",
    "farsali.apps.navegacion",
    "django_celery_results",
    "django_celery_beat",
]

# Config. de correo
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "farsalicolombia@gmail.com"
EMAIL_HOST_PASSWORD = "gbmjmcjnaupknyec"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Config. keys CAPTCHA

GOOGLE_KEY_CAPTCHA_V3 = "6LeF1OQZAAAAANEM_w4Boie-wolB4a3rxnu5D1-u"
GOOGLE_SECRET_KEY_CAPTCHA_V3 = "6LeF1OQZAAAAAD26pvXzsOWkilGTkUNlMtT3ZaOg"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = "farsali.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.media",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "farsali.context_processors.farsali",
            ],
        },
    },
]

WSGI_APPLICATION = "farsali.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "desq37k94ie0gg",
        "USER": "u75o6o7t5qfsmu",
        "PASSWORD": "pdb0ff401966f34bab34be1ba2327080cd653ca39e334247a1456b7564ae86a2a",
        "HOST": "ec2-3-86-117-9.compute-1.amazonaws.com",
        "PORT": 5432,
    }
}

# postgres://bgccaiwpigbefl:1161727a46f04ded0eb0fca1dfbacc71c02ff17ee459383c0255bec1db01c190@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d1p7nglrlkcon5

# postgres://u75o6o7t5qfsmu:pdb0ff401966f34bab34be1ba2327080cd653ca39e334247a1456b7564ae86a2a@ec2-3-86-117-9.compute-1.amazonaws.com:5432/desq37k94ie0gg


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "es"

LANGUAGES = (
    ("es", _("Espanol")),
    ("en", _("Ingles")),
    ("ca", _("Catala")),
    ("de", _("Aleman")),
    ("it", _("Italiano")),
    ("nl", _("Holandes")),
    ("fr", _("Frances")),
    ("pt", _("Portugues")),
    ("ru", _("Ruso")),
    ("sv", _("Sueco")),
    ("zh", _("Chino")),
    ("ja", _("Japones")),
    ("da", _("Danes")),
    ("ar", _("Arabe")),
    ("id", _("Indonesio")),
    ("ko", _("Coreano")),
    ("ms", _("Malayo")),
    ("no", _("Noruego")),
    ("tl", _("Tagalo")),
    ("th", _("Tailandes")),
    ("tr", _("Turco")),
    ("vi", _("Vietnamita")),
)

# S3 CONFIG

AWS_ACCESS_KEY_ID = "AKIAQ76SOCLW25DOY754"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "farsali-col-bucket"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = "us-east-2"
AWS_QUERYSTRING_AUTH = False

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# MESSAGE DJANGO
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = "uploads"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

try:
    from .local_settings import *  # noqa
except ImportError:
    pass

django_heroku.settings(locals())


# Api keys of mercadopagos
MERCADOPAGO_URL = "https://api.mercadopago.com/v1/payments/"
MERCADOPAGO_PUBLIC_KEY = "APP_USR-3631e183-eff4-474e-8f32-704eccc16578"
MERCADOPAGO_ACCESS_TOKEN = (
    "APP_USR-1611010299166741-092904-c7a74b63ba851707b3925261263f3ed4-652583311"
)
MERCADOPAGO_CLIENT_ID = "1611010299166741"
MERCADOPAGO_CLIENT_SECRET = "CCrznaGLOIf33iM6arHjHFP5hlhv7FAv"
""" 
if DEBUG:
    MERCADOPAGO_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY_TEST")
    MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN_TEST") """


# Api keys of wompi
WOMPI_PUBLIC_KEY = os.environ.get("WOMPI_PUBLIC_KEY_PROD")
WOMPI_PRIVATE_KEY = os.environ.get("WOMPI_PRIVATE_KEY_PROD")

if DEBUG:
    WOMPI_PUBLIC_KEY = os.environ.get("WOMPI_PUBLIC_KEY_TEST")
    WOMPI_PRIVATE_KEY = os.environ.get("WOMPI_PRIVATE_KEY_TEST")


# Api keys of epayco
EPAYCO_PUBLIC_KEY = os.environ.get("EPAYCO_PUBLIC_KEY_PROD")

if DEBUG:
    EPAYCO_PUBLIC_KEY = os.environ.get("EPAYCO_PUBLIC_KEY_TEST")


# Config Admin Material
MATERIAL_ADMIN_SITE = {
    "HEADER": "Farsali Control",
    "TITLE": "Farsali Control Portal",
    "FAVICON": "path/to/favicon",  # Admin site favicon (path to static should be specified)
    # "MAIN_BG_COLOR": "#f8bd3e",
    # "MAIN_HOVER_COLOR": "#f8bd3e",
    # 'PROFILE_PICTURE':  'path/to/image',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG':  'path/to/image',  # Admin site profile background (path to static should be specified)
    "LOGIN_LOGO": "images/logo-my-farsali.png",  # Admin site logo on login page
    "LOGOUT_BG": "",  # Admin site background on login/logout pages (path to static should be specified)
    "SHOW_COUNTS": True,
    "APP_ICONS": {},
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Redis
REDIS_PASSWORD = env.str(
    "REDIS_PASSWORD", "p62810ddbc7b624ce10f7e79261ea77ad20668ada8c8171a4b50a1a4c68358495"
)
REDIS_HOST = env.str("REDIS_HOST", "ec2-54-87-81-33.compute-1.amazonaws.com")
REDIS_PORT = env.str("REDIS_PORT", "12520")
REDIS_TLS_URL = env.str(
    "REDIS_TLS_URL",
    "redis://:p62810ddbc7b624ce10f7e79261ea77ad20668ada8c8171a4b50a1a4c68358495@ec2-54-87-81-33.compute-1.amazonaws.com:12520",
)

REDIS_URL_PRE = REDIS_TLS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_TLS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": None,
    }
}

# Sessions con redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

BROKER_URL = "amqp://guest:guest@localhost:5672//"

CELERY_BROKER_URL = REDIS_URL_PRE
CELERY_RESULT_BACKEND = REDIS_URL_PRE
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Bogota"
