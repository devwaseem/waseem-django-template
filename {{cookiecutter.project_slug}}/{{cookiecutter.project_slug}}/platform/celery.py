"""Celery bootstrap with request correlation propagated into task logs."""

from __future__ import annotations

import os
from typing import Any

from celery import Celery
from celery.signals import before_task_publish, task_postrun, task_prerun
from structlog.contextvars import bind_contextvars, get_contextvars, reset_contextvars

from {{ cookiecutter.project_slug }}.platform.request_id import (
    CELERY_REQUEST_ID_HEADER,
    is_valid_request_id,
)
from {{ cookiecutter.project_slug }}.platform.telemetry import initialize_telemetry


project_package = __name__.partition(".")[0]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_package}.settings.dev")
initialize_telemetry()

app = Celery(project_package)
app.config_from_object(f"{__package__}.celeryconfig")
app.autodiscover_tasks()

_task_context_tokens: dict[str, dict[str, Any]] = {}


@before_task_publish.connect
def attach_request_id(headers: dict[str, Any] | None = None, **_kwargs: Any) -> None:
    """Carry the active request ID into every task published from that request."""
    if headers is None:
        return
    request_id = get_contextvars().get("request_id")
    if is_valid_request_id(request_id):
        headers[CELERY_REQUEST_ID_HEADER] = request_id


@task_prerun.connect
def bind_task_context(task_id: str, task: object, **_kwargs: Any) -> None:
    """Expose correlation fields to structured logs emitted by a task body."""
    headers = getattr(getattr(task, "request", None), "headers", None) or {}
    context: dict[str, Any] = {"task_id": task_id}
    request_id = headers.get(CELERY_REQUEST_ID_HEADER)
    if is_valid_request_id(request_id):
        context["request_id"] = request_id
    _task_context_tokens[task_id] = bind_contextvars(**context)


@task_postrun.connect
def clear_task_context(task_id: str, **_kwargs: Any) -> None:
    """Reset task-local context so long-lived workers cannot leak correlation IDs."""
    tokens = _task_context_tokens.pop(task_id, None)
    if tokens is not None:
        reset_contextvars(**tokens)
