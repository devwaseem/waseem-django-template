"""Private, low-cardinality Prometheus metrics for application HTTP traffic."""

from __future__ import annotations

from hmac import compare_digest
from time import perf_counter
from typing import Protocol

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest


OBSERVABILITY_PATHS = frozenset({"/livez/", "/metrics/", "/readyz/"})
METRIC_LABELS = ("method", "route", "status_code")
HTTP_REQUESTS = Counter(
    "http_server_requests_total",
    "Completed application HTTP requests.",
    METRIC_LABELS,
)
HTTP_REQUEST_DURATION = Histogram(
    "http_server_request_duration_seconds",
    "End-to-end application HTTP request duration in seconds.",
    METRIC_LABELS,
)


class ResponseCallable(Protocol):
    """Define the synchronous Django middleware response contract."""

    def __call__(self, request: HttpRequest) -> HttpResponse: ...


def route_label(request: HttpRequest) -> str:
    """Use Django's route pattern rather than a user-controlled URL path."""
    route = getattr(getattr(request, "resolver_match", None), "route", "")
    return route or "unmatched"


def record_http_request(
    request: HttpRequest,
    *,
    duration_seconds: float,
    status_code: int,
) -> None:
    """Record one bounded-label HTTP outcome for a completed request."""
    labels = {
        "method": request.method,
        "route": route_label(request),
        "status_code": str(status_code),
    }
    HTTP_REQUESTS.labels(**labels).inc()
    HTTP_REQUEST_DURATION.labels(**labels).observe(duration_seconds)


def has_metrics_access(request: HttpRequest) -> bool:
    """Require the configured bearer token without accepting query credentials."""
    token = settings.METRICS_TOKEN
    authorization = request.headers.get("Authorization", "")
    prefix = "Bearer "
    if not token or not authorization.startswith(prefix):
        return False
    return compare_digest(authorization.removeprefix(prefix), token)


@require_GET
def metrics(request: HttpRequest) -> HttpResponse:
    """Expose the Prometheus registry only to an explicitly enabled scraper."""
    if not settings.METRICS_ENABLED:
        raise Http404
    if not has_metrics_access(request):
        return HttpResponse(status=403)
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


class HttpMetricsMiddleware:
    """Measure application routes while excluding probes and metric scrapes."""

    def __init__(self, get_response: ResponseCallable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not settings.METRICS_ENABLED or request.path in OBSERVABILITY_PATHS:
            return self.get_response(request)
        started_at = perf_counter()
        try:
            response = self.get_response(request)
        except Exception:
            record_http_request(
                request,
                duration_seconds=perf_counter() - started_at,
                status_code=500,
            )
            raise
        record_http_request(
            request,
            duration_seconds=perf_counter() - started_at,
            status_code=response.status_code,
        )
        return response
