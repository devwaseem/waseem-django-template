from django.http.request import HttpRequest

from server.apps.main.helpers.network import get_ip_from_request
from server.settings.components.caches import RATE_LIMIT_CACHE_BACKEND

RATELIMIT_USE_CACHE = RATE_LIMIT_CACHE_BACKEND


def RATELIMIT_IP_META_KEY(request: HttpRequest) -> str | None:  # noqa
    return get_ip_from_request(request=request)
