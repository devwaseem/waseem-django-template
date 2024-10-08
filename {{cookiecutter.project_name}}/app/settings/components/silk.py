# Django Silk
# https://github.com/jazzband/django-silk

from app.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)

INSTALLED_APPS += ["silk"]
MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
SILKY_PYTHON_PROFILER = True
