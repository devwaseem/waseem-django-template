"""Small, dependency-free process and dependency health checks."""

from __future__ import annotations

from django.conf import settings
from django.core.cache import cache
from django.db import connections
from django.http import HttpRequest, JsonResponse


def livez(_request: HttpRequest) -> JsonResponse:
    """Report that the ASGI process is able to serve requests."""
    return JsonResponse({"status": "ok"})


def version(_request: HttpRequest) -> JsonResponse:
    """Expose non-sensitive build identity for support and incident response."""
    return JsonResponse(
        {
            "version": settings.APP_VERSION,
            "build_sha": settings.APP_BUILD_SHA,
            "template_version": settings.TEMPLATE_VERSION,
            "rendering_mode": settings.RENDERING_MODE,
        }
    )


def readyz(_request: HttpRequest) -> JsonResponse:
    """Report readiness only after Postgres and Redis are reachable."""
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
        cache.set("platform:healthcheck", "ok", timeout=5)
        if cache.get("platform:healthcheck") != "ok":
            raise RuntimeError("Redis did not return the health-check value.")
    except Exception:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})
