"""The versioned Django Ninja API and its uniform error envelope."""

from __future__ import annotations

import logging

from django.http import Http404, HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, HttpError, ValidationError

from {{ cookiecutter.project_slug }}.api.auth import problem, router as auth_router
from {{ cookiecutter.project_slug }}.domains.registry import register_api


logger = logging.getLogger(__name__)
api = NinjaAPI(
    title="{{ cookiecutter.project_name }} API",
    version="1.0.0",
    urls_namespace="{{ cookiecutter.project_slug }}_api",
)
api.add_router("/auth", auth_router)
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
