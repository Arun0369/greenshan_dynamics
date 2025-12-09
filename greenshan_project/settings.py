"""
Django settings for greenshan_project project.
"""

from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "replace-this-with-a-secure-key"

# DEVELOPMENT MODE
DEBUG = True

ALLOWED_HOSTS = []


# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Our app
    "greenshan",
]
INSTALLED_APPS += [
    'django.contrib.sites',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'qrcode',
    
]
SITE_ID = 1





# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# -------------------------------------------------------------------
# URLS
# -------------------------------------------------------------------

ROOT_URLCONF = "greenshan_project.urls"


# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],     # template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # required
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -------------------------------------------------------------------
# WSGI
# -------------------------------------------------------------------

WSGI_APPLICATION = "greenshan_project.wsgi.application"


# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# -------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = []


# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"   # Indian timezone

USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]       # static/ folder
STATIC_ROOT = BASE_DIR / "staticfiles"         # for collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"                # for uploads


# -------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -------------------------------------------------------------------
# EMAIL BACKEND (development mode)
# -------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = '/manage/'
LOGOUT_REDIRECT_URL = '/manage/login/'