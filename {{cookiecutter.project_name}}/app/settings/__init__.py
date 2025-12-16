from typing import TYPE_CHECKING

import django_stubs_ext
from split_settings.tools import include

from app.settings.flags import (
    DEBUG,
    ENABLE_CPROFILE,
    ENABLE_HEALTH_CHECK,
    ENABLE_PYINSTRUMENT,
    ENABLE_SENTRY,
    ENABLE_SILK_PROFILING,
)

django_stubs_ext.monkeypatch()

if TYPE_CHECKING:
    from celery.app.task import Task

    Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined] # noqa

# Django settings
# Include it first before third party

include(
    "components/common.py",
    "components/caches.py",
    "components/database.py",
    "components/storages.py",
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
