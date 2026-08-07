"""Narrow, auditable policy for Django admin impersonation."""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from hijack import signals
from structlog.contextvars import get_contextvars

from {{ cookiecutter.project_slug }}.platform.models import (
    AdminImpersonationAuditEvent,
    User,
)
from {{ cookiecutter.project_slug }}.platform.request_id import is_valid_request_id


def can_hijack(*, hijacker: User, hijacked: User) -> bool:
    """Permit only an enabled superuser to impersonate a regular active user."""
    return (
        settings.ENABLE_ADMIN_HIJACK
        and hijacker.is_active
        and hijacker.is_superuser
        and hijacked.is_active
        and not hijacked.is_staff
        and not hijacked.is_superuser
    )


def record_impersonation_event(
    *,
    action: AdminImpersonationAuditEvent.Action,
    actor: User,
    target: User,
    request: HttpRequest,
) -> None:
    """Persist minimal correlation data without trusting forwarded IP headers."""
    request_id = get_contextvars().get("request_id")
    if not is_valid_request_id(request_id):
        request_id = ""

    remote_address = request.META.get("REMOTE_ADDR") or None
    AdminImpersonationAuditEvent.objects.create(
        action=action,
        actor=actor,
        target=target,
        ip_address=remote_address,
        request_id=request_id,
    )


@receiver(signals.hijack_started)
def record_hijack_started(
    sender: type[object],
    hijacker: User,
    hijacked: User,
    request: HttpRequest,
    **kwargs: Any,
) -> None:
    """Record the start of each successfully authorized impersonation session."""
    record_impersonation_event(
        action=AdminImpersonationAuditEvent.Action.STARTED,
        actor=hijacker,
        target=hijacked,
        request=request,
    )


@receiver(signals.hijack_ended)
def record_hijack_ended(
    sender: type[object],
    hijacker: User,
    hijacked: User,
    request: HttpRequest,
    **kwargs: Any,
) -> None:
    """Record the release of an impersonation session with the same safeguards."""
    record_impersonation_event(
        action=AdminImpersonationAuditEvent.Action.ENDED,
        actor=hijacker,
        target=hijacked,
        request=request,
    )
