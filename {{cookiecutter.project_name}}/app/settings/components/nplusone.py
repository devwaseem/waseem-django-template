# https://github.com/jmcarp/nplusone

import logging

import structlog

from app.settings.components.common import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += [
    "nplusone.ext.django",
]

MIDDLEWARE = [
    "nplusone.ext.django.NPlusOneMiddleware",
    *MIDDLEWARE,
]

# Logging N+1 requests:
# NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests # noqa
NPLUSONE_LOGGER = structlog.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARNING
NPLUSONE_WHITELIST = [{"model": "admin.LogEntry", "field": "user"}]
