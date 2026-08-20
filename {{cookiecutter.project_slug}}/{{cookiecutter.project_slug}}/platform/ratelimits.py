"""Shared, Redis-backed application rate-limit policies."""

from __future__ import annotations

from collections.abc import Callable
from math import ceil
from typing import Literal

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django_ratelimit.core import get_usage


RateLimitKey = str | Callable[[str, HttpRequest], str]
PublicAuthAction = Literal["login", "registration", "password_reset"]

AUTH_RATE_SETTINGS: dict[PublicAuthAction, tuple[str, str]] = {
    "login": ("RATE_LIMIT_LOGIN_IP", "RATE_LIMIT_LOGIN_ACCOUNT"),
    "registration": (
        "RATE_LIMIT_REGISTRATION_IP",
        "RATE_LIMIT_REGISTRATION_ACCOUNT",
    ),
    "password_reset": (
        "RATE_LIMIT_PASSWORD_RESET_IP",
        "RATE_LIMIT_PASSWORD_RESET_ACCOUNT",
    ),
}


class RateLimitExceeded(PermissionDenied):
    """A blocked request with a safe client retry interval."""

    def __init__(self, *, retry_after: int) -> None:
        super().__init__("Request rate limit exceeded.")
        self.retry_after = retry_after


def enforce_rate_limit(
    request: HttpRequest,
    *,
    group: str,
    key: RateLimitKey,
    rate: str,
) -> None:
    """Increment one counter and stop a request when it exceeds its policy."""
    retry_after = rate_limit_retry_after(
        request,
        group=group,
        key=key,
        rate=rate,
    )
    if retry_after is not None:
        raise RateLimitExceeded(retry_after=retry_after)


def rate_limit_retry_after(
    request: HttpRequest,
    *,
    group: str,
    key: RateLimitKey,
    rate: str,
) -> int | None:
    """Increment one counter and return a retry interval when it is exhausted."""
    usage = get_usage(request, group=group, key=key, rate=rate, increment=True)
    if usage is None or not usage["should_limit"]:
        return None

    return max(1, ceil(float(usage["time_left"])))


def enforce_public_auth_rate_limits(
    request: HttpRequest,
    *,
    action: PublicAuthAction,
    email: str,
) -> None:
    """Apply independent IP and normalized-account limits to public auth flows."""
    ip_setting, account_setting = AUTH_RATE_SETTINGS[action]
    normalized_email = email.strip().casefold()

    def account_key(_group: str, _request: HttpRequest) -> str:
        return normalized_email

    enforce_rate_limit(
        request,
        group=f"public-auth:{action}:ip",
        key="ip",
        rate=getattr(settings, ip_setting),
    )
    enforce_rate_limit(
        request,
        group=f"public-auth:{action}:account",
        key=account_key,
        rate=getattr(settings, account_setting),
    )
