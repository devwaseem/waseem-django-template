"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `development`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""


import django_stubs_ext
from celery.app.task import Task
from split_settings.tools import include

from app.settings.vars import (
    DEBUG,
    ENABLE_CPROFILE,
    ENABLE_HEALTH_CHECK,
    ENABLE_PYINSTRUMENT,
    ENABLE_SENTRY,
    ENABLE_SILK_PROFILING,
)

django_stubs_ext.monkeypatch()
Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined] # noqa

# Django settings
# Include it first before third party

include(
    "components/common.py",
    "components/caches.py",
    "components/database.py",
    "components/storages.py",
    "components/static.py",
    "components/logging.py",
    "components/emails.py",
    "components/security.py",
)

# Third-party:
include(
    "components/allauth.py",
    "components/auth.py",
    "components/aws.py",
    "components/csp.py",
    "components/constance.py",
    "components/dbbackup.py",
    "components/mjml.py",
    "components/rate_limit.py",
    "components/rest_framework.py",
)

if ENABLE_HEALTH_CHECK:
    include("components/health_check.py")

if ENABLE_SILK_PROFILING:
    include("components/silk.py")

if ENABLE_CPROFILE:
    include("components/cprofile.py")

if ENABLE_PYINSTRUMENT:
    include("components/pyinstrument.py")

if ENABLE_SENTRY:
    include("components/sentry.py")

# only for dev
if DEBUG:
    include(
        "components/nplusone.py",
        "components/debug_toolbar.py",
    )
