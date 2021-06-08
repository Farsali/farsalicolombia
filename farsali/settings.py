# coding: utf-8
import os

import django_heroku
from django import http
from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

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
    "localhost",
    "www.farsalicolombia.com",
    "farsalicolombia.com",
    "polar-tor-89642.herokuapp.com",
    "127.0.0.1",
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
    "farsali.apps",
    "farsali.apps.clientes",
    "farsali.apps.inventario",
    "farsali.apps.ventas",
    "farsali.apps.navegacion",
    "rangefilter",
    "sorl.thumbnail",
    "storages",
]

# Config. de correo
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "farsalicolombia@gmail.com"
EMAIL_HOST_PASSWORD = "FarsaliCo2021"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Config. keys CAPTCHA

GOOGLE_KEY_CAPTCHA_V3 = "6LeF1OQZAAAAANEM_w4Boie-wolB4a3rxnu5D1-u"
GOOGLE_SECRET_KEY_CAPTCHA_V3 = "6LeF1OQZAAAAAD26pvXzsOWkilGTkUNlMtT3ZaOg"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
MERCADOPAGO_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY_PROD")
MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN_PROD")
MERCADOPAGO_CLIENT_ID = "1611010299166741"
MERCADOPAGO_CLIENT_SECRET = "CCrznaGLOIf33iM6arHjHFP5hlhv7FAv"

if DEBUG:
    MERCADOPAGO_PUBLIC_KEY = os.environ.get("MERCADOPAGO_PUBLIC_KEY_TEST")
    MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN_TEST")


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
