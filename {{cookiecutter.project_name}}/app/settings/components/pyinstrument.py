# https://pypi.org/project/pyinstrument/3.0.0b3/#profile-a-web-request-in-django

from django.utils.csp import CSP

from app.settings.components.common import MIDDLEWARE
from app.settings.components.csp import SECURE_CSP

MIDDLEWARE += ["pyinstrument.middleware.ProfilerMiddleware"]

# Temporary workaround until Pyinstrument supports CSP
SECURE_CSP["script-src"].append(CSP.UNSAFE_INLINE)
