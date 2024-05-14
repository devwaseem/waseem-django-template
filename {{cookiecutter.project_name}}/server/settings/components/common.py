"""Django settings for {{cookiecutter.project_verbose_name}}.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from env import Env

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
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
    # Health checks:
    # You may want to enable other checks as well,
    # see: https://github.com/KristianOellegaard/django-health-check
    # "health_check",
    # "health_check.db",
    # "health_check.cache",
    # "health_check.storage",
    # django-widget-tweaks
    # "widget_tweaks",
    # Django feather (Feather icons)
    # "django_feather",
    # Django HTMX
    # "django_htmx",
    # django-phonenumber-field
    # "phonenumber_field", Uncomment to enable
    # https://github.com/theatlantic/django-nested-admin
    # "nested_admin",
    # https://github.com/liminspace/django-mjml
    # "mjml",
    # https://github.com/SmileyChris/easy-thumbnails
    # "easy_thumbnails",
    # https://github.com/pmclanahan/django-celery-email
    # "djcelery_email",
    # "rest_framework",
    # "drf_spectacular",
]

PROJECT_APPS: list[str] = [
    "server.apps.main",
]

ALL_AUTH_APPS: list[str] = [
    # NOTE: Uncomment below lines to enable authentication
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
]

INSTALLED_APPS = [
    *ADMIN_APPS,
    *DEFAULT_DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *PROJECT_APPS,
    *ALL_AUTH_APPS,
]

MIDDLEWARE: list[str] = [
    # Logging:
    # "server.middleware.disable_client_side_caching_middleware", # Uncomment this line to disable client side caching
    # "django.middleware.cache.UpdateCacheMiddleware",  # This must be first on the list
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
    # "django.middleware.cache.FetchFromCacheMiddleware",  # This must be last
]

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
            / "server"
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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


LOGIN_URL = reverse_lazy("account_login")
LOGIN_REDIRECT_URL = "/"

# Session

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = "static"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR /  'dist',
]

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
    (Env("MJML_HOST"), Env("MJML_PORT", int, 28101)),
]
