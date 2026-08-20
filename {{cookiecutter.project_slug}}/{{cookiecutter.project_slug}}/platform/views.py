"""Framework-level HTML error views shared by server-rendered pages."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited

from {{ cookiecutter.project_slug }}.platform.ratelimits import RateLimitExceeded


def handler403(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    """Render a non-enumerating 403 or 429 response for HTML requests."""
    if isinstance(exception, (RateLimitExceeded, Ratelimited)):
        response = render(request, "errors/429.html", status=429)
        if isinstance(exception, RateLimitExceeded):
            response["Retry-After"] = str(exception.retry_after)
        return response
    return render(request, "errors/403.html", status=403)


def handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render the accessible HTML not-found page."""
    return render(request, "errors/404.html", status=404)


def handler500(request: HttpRequest) -> HttpResponse:
    """Render the accessible HTML server-error page."""
    return render(request, "errors/500.html", status=500)
