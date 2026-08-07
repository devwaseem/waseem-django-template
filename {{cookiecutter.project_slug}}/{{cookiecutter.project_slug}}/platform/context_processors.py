"""Small template context additions that are safe for every request."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest


def account_settings(_request: HttpRequest) -> dict[str, bool]:
    """Expose the env-controlled registration capability to auth templates."""
    return {"ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION}
