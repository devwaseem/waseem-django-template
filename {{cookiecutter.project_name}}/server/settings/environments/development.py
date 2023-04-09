import logging
import os
import socket

import structlog

from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.csp import (
    CSP_CONNECT_SRC,
    CSP_DEFAULT_SRC,
    CSP_SCRIPT_SRC,
    CSP_STYLE_SRC,
)
from server.settings.components.logging import LOGGING


def get_host_ip_address() -> str:
    ip_address_list = socket.gethostbyname_ex(socket.gethostname())[2]
    try:
        if len(ip_address_list) > 1:
            return ip_address_list[1]
        return ip_address_list[0]
    except socket.gaierror:
        return "0.0.0.0"


DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-47gh%z!d^2#@q(vp17ppxwg=f)iblmojmgq*j#pqs-4+@a2_yl"

BASE_URL = "http://localhost:8000"

# ALLOWED_HOSTS = [
#     "localhost",
#     "0.0.0.0",
#     "127.0.0.1",
#     "[::1]",
#     "192.168.0.155",
# ]  # noqa: S104

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
    "django_browser_reload",
    "nplusone.ext.django",
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "{{cookiecutter.project_name}}"),
        "USER": os.environ.get("POSTGRES_USER", "{{cookiecutter.project_name}}"),
        "PASSWORD": os.environ.get(
            "POSTGRES_PASSWORD", "{{cookiecutter.project_name}}"
        ),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DATABASE_PORT", 5432),
        "CONN_MAX_AGE": os.environ.get("CONN_MAX_AGE", 1),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

CACHES = {
    "default": {
        # like https://github.com/jazzband/django-redis
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379",
    },
}

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# Django Vite
DJANGO_VITE_DEV_MODE = True
DJANGO_VITE_DEV_SERVER_HOST = get_host_ip_address()
DJANGO_VITE_DEV_SERVER_PORT = 5173

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_DEFAULT_SRC += (  # type: ignore[assignment]
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
    f"ws://{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)
CSP_SCRIPT_SRC += (  # type: ignore[assignment]
    "'self'",
    "ajax.googleapis.com",
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)
CSP_STYLE_SRC += (f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",)  # type: ignore[assignment]
CSP_CONNECT_SRC += (  # type: ignore[assignment]
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
    f"ws://{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)

# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = (
    "nplusone.ext.django.NPlusOneMiddleware",
) + MIDDLEWARE  # noqa  # noqa: WPS440

# Logging N+1 requests:
# NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = structlog.getLogger("django")  # noqa
NPLUSONE_LOG_LEVEL = logging.WARN  # type:ignore
NPLUSONE_WHITELIST = [{"model": "admin.LogEntry", "field": "user"}]


# Browser Reload Middleware
MIDDLEWARE += ("django_browser_reload.middleware.BrowserReloadMiddleware",)


LOGGING["loggers"]["server.apps.main"] = {  # type: ignore[index]
    "handlers": ["plain_console"],
    "propagate": False,
    "level": "DEBUG",
}


LOGGING["loggers"]["django"] = {  # type: ignore[index]
    "handlers": ["plain_console"],
    "propagate": False,
    "level": "INFO",
}

# LOGGING["loggers"]["django.template"] = {  # type: ignore[index]
#     "handlers": ["plain_console"],
#     "propagate": False,
#     "level": "DEBUG",
# }

# Django CProfile
MIDDLEWARE += ("django_cprofile_middleware.middleware.ProfilerMiddleware",)
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

# Django Silk
# INSTALLED_APPS += ["silk"]
# MIDDLEWARE += ("silk.middleware.SilkyMiddleware",)


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 1025
