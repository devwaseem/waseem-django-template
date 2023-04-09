"""Django settings for {{cookiecutter.project_verbose_name}}.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

from server.settings import BASE_DIR

DEBUG = False

BASE_URL = "https://{{cookiecutter.project_domain}}"

# Application definition

ADMIN_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
]

DEFAULT_DJANGO_APPS: list[str] = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS: list[str] = [
    "django_vite",
    # Health checks:
    # You may want to enable other checks as well,
    # see: https://github.com/KristianOellegaard/django-health-check
    # "health_check",
    # "health_check.db",
    # "health_check.cache",
    # "health_check.storage",
    # django-widget-tweaks
    "widget_tweaks",
    # Django feather (Feather icons)
    "django_feather",
    # Django HTMX
    "django_htmx",
    # Django-sekizai
    "sekizai",
    # django-phonenumber-field
    "phonenumber_field",
    # https://github.com/theatlantic/django-nested-admin
    "nested_admin",
    # https://github.com/liminspace/django-mjml
    "mjml",
    # https://github.com/SmileyChris/easy-thumbnails
    "easy_thumbnails",
]

PROJECT_APPS: list[str] = [
    "server.apps.main",
]

INSTALLED_APPS = [
    *ADMIN_APPS,
    *DEFAULT_DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *PROJECT_APPS,
]

MIDDLEWARE: tuple[str, ...] = (
    # Logging:
    # "server.settings.components.logging.LoggingContextVarsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    # Content Security Policy:
    "csp.middleware.CSPMiddleware",
    # Django:
    "django.middleware.security.SecurityMiddleware",
    # django-permissions-policy
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Django HTTP Referrer Policy:
    "django_http_referrer_policy.middleware.ReferrerPolicyMiddleware",
    # Django HTMX
    "django_htmx.middleware.HtmxMiddleware",
)

ROOT_URLCONF = "server.urls"

# Templates
# https://docs.djangoproject.com/en/3.2/ref/templates/api

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Contains plain text templates, like `robots.txt`:
            BASE_DIR
            / "config"
            / "templates",
        ],
        "OPTIONS": {
            "context_processors": [
                # Default template context processors:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                # django-sekizai
                "sekizai.context_processors.sekizai",
                # Django CSP
                "csp.context_processors.nonce",
                # Custom
                "server.apps.main.context_processors.get_site_data",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

APPEND_SLASH = True

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_USER_MODEL = "main.User"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_TZ = True

TIME_ZONE = "UTC"

LANGUAGES = (("en", _("English")),)

USE_I18N = False

USE_L10N = True

DATE_INPUT_FORMATS = ("%d-%m-%Y", "%Y-%m-%d")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FRONTEND_STATIC_SOURCE_DIR = BASE_DIR / "frontend"

DJANGO_VITE_ASSETS_PATH = FRONTEND_STATIC_SOURCE_DIR / "static"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = "static"

STATIC_URL = "/static/"

STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Media files
# Media root dir is commonly changed in production
# (see development.py and production.py).
# https://docs.djangoproject.com/en/3.2/topics/files/

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "same-origin"

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: dict[str, str | list[str]] = {}  # noqa: WPS234

# https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#phonenumber-default-region
PHONENUMBER_DEFAULT_REGION = "US"  # Defaults to India

# Login URL
LOGIN_URL = "main:login"

# Messages
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
MESSAGE_TAGS = {
    messages.DEBUG: "gray",
    messages.INFO: "blue",
    messages.SUCCESS: "green",
    messages.WARNING: "yellow",
    messages.ERROR: "red",
}

# MJML: https://github.com/liminspace/django-mjml#tcpserver-mode
MJML_BACKEND_MODE = "tcpserver"
MJML_TCPSERVERS = [
    (os.environ.get("MJML_HOST", default="localhost"), 28101),
]

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)
CELERY_IMPORTS = ("server.apps.main.tasks",)
