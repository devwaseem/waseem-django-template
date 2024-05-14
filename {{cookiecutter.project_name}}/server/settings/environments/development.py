import logging

import structlog

from server.settings.components.caches import CACHES
from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.logging import LOGGING

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-47gh%z!d^2#@q(vp17ppxwg=f)iblmojmgq*j#pqs-4+@a2_yl"
)

BASE_URL = "http://localhost:8000"


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

CACHES["default"]["BACKEND"] = "django.core.cache.backends.dummy.DummyCache"

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Django Browser Reload
MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]


# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = ["nplusone.ext.django.NPlusOneMiddleware", *MIDDLEWARE]

# Logging N+1 requests:
# NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests # noqa
NPLUSONE_LOGGER = structlog.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARNING  # type:ignore
NPLUSONE_WHITELIST = [{"model": "admin.LogEntry", "field": "user"}]


LOGGING["loggers"] = {
    "django.request": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    "django.server": {
        "handlers": ["plain_console"],
        "propagate": False,
        "level": "DEBUG",
    },
    "django.db": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    "django.core.cache": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    "django.template": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    "django.security": {
        "handlers": ["plain_console"],
        "level": "WARNING",
        "propagate": False,
    },
    "celery": {
        "handlers": ["plain_console"],
        "level": "INFO",
        "propagate": False,
    },
    "server": {
        "handlers": ["plain_console"],
        "level": "DEBUG",
        "propagate": True,
    },
}

"""
# Django CProfile
MIDDLEWARE += ["django_cprofile_middleware.middleware.ProfilerMiddleware"]
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False
"""

"""
# Django Silk
# INSTALLED_APPS += ["silk"]
# MIDDLEWARE += ("silk.middleware.SilkyMiddleware",)
"""

# dbbackup
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "./data"}
