from pathlib import Path
import os

# =================================================
# BASE DIRECTORY
# =================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =================================================
# SECURITY
# =================================================

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")

# ✅ IMPORTANT: Turn OFF in production
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]


# =================================================
# APPLICATIONS
# =================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "greenshan",
    'greenshan.apps.GreenshanConfig',
]


# =================================================
# MIDDLEWARE
# =================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # ✅ WhiteNoise should be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# =================================================
# URL & WSGI
# =================================================

ROOT_URLCONF = "greenshan_project.urls"
WSGI_APPLICATION = "greenshan_project.wsgi.application"


# =================================================
# TEMPLATES
# =================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =================================================
# DATABASE
# =================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =================================================
# INTERNATIONALIZATION
# =================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True


# =================================================
# STATIC FILES
# =================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ✅ WhiteNoise optimization
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =================================================
# MEDIA FILES
# =================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =================================================
# AUTH
# =================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/manage/dashboard/"
LOGOUT_REDIRECT_URL = "/"