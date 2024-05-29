# https://pypi.org/project/pyinstrument/3.0.0b3/#profile-a-web-request-in-django

from {{cookiecutter.project_name}}.settings.components.common import MIDDLEWARE
from {{cookiecutter.project_name}}.settings.components.csp import CSP_SCRIPT_SRC

MIDDLEWARE += ["pyinstrument.middleware.ProfilerMiddleware"]

# Temporary workaround until Pyinstrument supports CSP
CSP_SCRIPT_SRC += ("'unsafe-inline'",)

