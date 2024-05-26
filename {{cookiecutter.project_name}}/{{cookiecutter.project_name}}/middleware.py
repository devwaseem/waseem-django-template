from typing import Callable

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.cache import add_never_cache_headers


def disable_client_side_caching_middleware(
    get_response: Callable[[HttpRequest], HttpResponse],
) -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        add_never_cache_headers(response)
        return response

    return middleware
