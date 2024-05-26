# Django cprofile
# https://pypi.org/project/django-cprofile-middleware/

from {{cookiecutter.project_name}}.settings.components.common import (
    MIDDLEWARE,
)

MIDDLEWARE += ["django_cprofile_middleware.middleware.ProfilerMiddleware"]
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = True
