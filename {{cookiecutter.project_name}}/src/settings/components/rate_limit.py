from django.http.request import HttpRequest

from src.helpers.network import get_ip_from_request

RATELIMIT_HASH_ALGORITHM = "hashlib.md5"


def RATELIMIT_IP_META_KEY(request: HttpRequest) -> str | None:  # noqa
    return get_ip_from_request(request=request)
