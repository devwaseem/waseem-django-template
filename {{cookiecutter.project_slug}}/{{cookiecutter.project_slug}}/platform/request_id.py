"""Stable request identity for logs, responses, and task handoff."""

from __future__ import annotations

import re
from typing import Protocol
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from structlog.contextvars import bind_contextvars, reset_contextvars


REQUEST_ID_HEADER = "X-Request-ID"
CELERY_REQUEST_ID_HEADER = "x-request-id"
_REQUEST_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{7,127}")


class ResponseCallable(Protocol):
    def __call__(self, request: HttpRequest) -> HttpResponse: ...


def is_valid_request_id(value: object) -> bool:
    """Allow bounded, log-safe caller-supplied IDs and reject everything else."""
    return isinstance(value, str) and _REQUEST_ID_PATTERN.fullmatch(value) is not None


def request_id_from_header(value: object) -> str:
    """Use a trusted correlation ID or create a fresh opaque identifier."""
    return value if is_valid_request_id(value) else uuid4().hex


class RequestIDMiddleware:
    """Bind one request ID to structlog and return it to the client."""

    def __init__(self, get_response: ResponseCallable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request_id_from_header(request.headers.get(REQUEST_ID_HEADER))
        request.request_id = request_id
        tokens = bind_contextvars(request_id=request_id)
        try:
            response = self.get_response(request)
        finally:
            reset_contextvars(**tokens)
        response[REQUEST_ID_HEADER] = request_id
        return response
