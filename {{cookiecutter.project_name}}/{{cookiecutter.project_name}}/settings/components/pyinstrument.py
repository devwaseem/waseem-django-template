from django.http import HttpRequest
from optik_invoice.settings.components.common import MIDDLEWARE

MIDDLEWARE += ["pyinstrument.middleware.ProfilerMiddleware"]


def custom_show_pyinstrument(request: HttpRequest) -> bool:
    return request.user.is_superuser


PYINSTRUMENT_SHOW_CALLBACK = f"{__name__}.custom_show_pyinstrument"
