"""Django Ninja adapter for the shared API perimeter policy."""

from __future__ import annotations

from contextvars import ContextVar

from django.conf import settings
from django.http import HttpRequest
from ninja.throttling import BaseThrottle

from {{ cookiecutter.project_slug }}.platform.ratelimits import rate_limit_retry_after


retry_after_context: ContextVar[int | None] = ContextVar(
    "api_rate_limit_retry_after", default=None
)


class APIIPRateThrottle(BaseThrottle):
    """Apply one broad, atomic IP limit to every versioned API operation."""

    def allow_request(self, request: HttpRequest) -> bool:
        retry_after_context.set(
            rate_limit_retry_after(
                request,
                group="api:ip",
                key="ip",
                rate=settings.RATE_LIMIT_API_IP,
            )
        )
        return retry_after_context.get() is None

    def wait(self) -> int | None:
        """Return the request-local interval used by Ninja's 429 response."""
        return retry_after_context.get()
