"""The versioned Django Ninja API and its uniform error envelope."""

from __future__ import annotations

import logging

from django.http import Http404, HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, HttpError, Throttled, ValidationError

from {{ cookiecutter.project_slug }}.api.auth import problem, router as auth_router
from {{ cookiecutter.project_slug }}.api.throttling import APIIPRateThrottle
from {{ cookiecutter.project_slug }}.domains.registry import register_api
from {{ cookiecutter.project_slug }}.platform.ratelimits import RateLimitExceeded


logger = logging.getLogger(__name__)
api = NinjaAPI(
    title="{{ cookiecutter.project_name }} API",
    version="1.0.0",
    urls_namespace="{{ cookiecutter.project_slug }}_api",
    throttle=APIIPRateThrottle(),
)
api.add_router("/auth", auth_router, throttle=APIIPRateThrottle())
register_api(api)


@api.exception_handler(AuthenticationError)
def authentication_error(
    request: HttpRequest, _exception: AuthenticationError
) -> JsonResponse:
    return problem(
        request,
        status=401,
        code="authentication_required",
        title="Authentication required",
        detail="Provide a valid bearer token.",
    )


@api.exception_handler(RateLimitExceeded)
def rate_limit_error(
    request: HttpRequest, exception: RateLimitExceeded
) -> JsonResponse:
    response = problem(
        request,
        status=429,
        code="rate_limited",
        title="Too many requests",
        detail="Wait before trying this request again.",
    )
    response["Retry-After"] = str(exception.retry_after)
    return response


@api.exception_handler(Throttled)
def throttled_error(request: HttpRequest, exception: Throttled) -> JsonResponse:
    response = problem(
        request,
        status=429,
        code="rate_limited",
        title="Too many requests",
        detail="Wait before trying this request again.",
    )
    if exception.wait is not None:
        response["Retry-After"] = str(exception.wait)
    return response


@api.exception_handler(ValidationError)
def validation_error(request: HttpRequest, _exception: ValidationError) -> JsonResponse:
    return problem(
        request,
        status=422,
        code="validation_error",
        title="Validation failed",
        detail="One or more fields are invalid.",
    )


@api.exception_handler(HttpError)
def http_error(request: HttpRequest, exception: HttpError) -> JsonResponse:
    return problem(
        request,
        status=exception.status_code,
        code="request_rejected",
        title="Request rejected",
        detail=str(exception.message),
    )


@api.exception_handler(Http404)
def not_found(request: HttpRequest, _exception: Http404) -> JsonResponse:
    return problem(
        request,
        status=404,
        code="not_found",
        title="Not found",
        detail="The requested resource does not exist.",
    )


@api.exception_handler(Exception)
def unhandled_error(request: HttpRequest, _exception: Exception) -> JsonResponse:
    logger.exception("api.unhandled_error")
    return problem(
        request,
        status=500,
        code="internal_error",
        title="Internal server error",
        detail="An unexpected error occurred.",
    )
