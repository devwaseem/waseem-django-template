"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""


import django_stubs_ext
from split_settings.tools import include

from {{cookiecutter.project_name}}.settings.vars import (
    DEBUG,
    ENABLE_CPROFILE,
    ENABLE_HEALTH_CHECK,
    ENABLE_SILK_PROFILING,
    ENABLE_PYINSTRUMENT,
    ENABLE_SENTRY
)

django_stubs_ext.monkeypatch()

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
    "components/sentry.py",
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
