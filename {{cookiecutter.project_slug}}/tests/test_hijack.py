from __future__ import annotations

import pytest
from django.contrib.admin.sites import site
from django.test import RequestFactory, override_settings
from structlog.contextvars import bind_contextvars, reset_contextvars

from {{ cookiecutter.project_slug }}.platform.hijack import (
    can_hijack,
    record_hijack_ended,
    record_hijack_started,
)
from {{ cookiecutter.project_slug }}.platform.models import (
    AdminImpersonationAuditEvent,
    User,
)


@pytest.mark.django_db
def test_admin_hijack_policy_allows_only_an_enabled_superuser() -> None:
    actor = User.objects.create_superuser(
        "admin@example.test",
        "Correct-horse-battery-1",
    )
    target = User.objects.create_user(
        "member@example.test",
        "Correct-horse-battery-1",
    )
    staff_target = User.objects.create_user(
        "staff@example.test",
        "Correct-horse-battery-1",
        is_staff=True,
    )

    assert can_hijack(hijacker=actor, hijacked=target) is False
    with override_settings(ENABLE_ADMIN_HIJACK=True):
        assert can_hijack(hijacker=actor, hijacked=target) is True
        assert can_hijack(hijacker=actor, hijacked=staff_target) is False
        assert can_hijack(hijacker=target, hijacked=actor) is False
        target.is_active = False
        target.save(update_fields=["is_active"])
        assert can_hijack(hijacker=actor, hijacked=target) is False


@pytest.mark.django_db
def test_admin_hijack_events_are_append_only_and_correlated(
    rf: RequestFactory,
) -> None:
    actor = User.objects.create_superuser(
        "admin@example.test",
        "Correct-horse-battery-1",
    )
    target = User.objects.create_user(
        "member@example.test",
        "Correct-horse-battery-1",
    )
    started_request = rf.post("/hijack/acquire/", REMOTE_ADDR="203.0.113.10")
    tokens = bind_contextvars(request_id="hijack-20260807")
    try:
        record_hijack_started(
            sender=object,
            hijacker=actor,
            hijacked=target,
            request=started_request,
        )
    finally:
        reset_contextvars(**tokens)

    ended_request = rf.post("/hijack/release/")
    ended_request.META.pop("REMOTE_ADDR")
    record_hijack_ended(
        sender=object,
        hijacker=actor,
        hijacked=target,
        request=ended_request,
    )

    events = list(AdminImpersonationAuditEvent.objects.order_by("occurred_at"))
    assert [(event.action, event.actor, event.target) for event in events] == [
        (AdminImpersonationAuditEvent.Action.STARTED, actor, target),
        (AdminImpersonationAuditEvent.Action.ENDED, actor, target),
    ]
    assert events[0].ip_address == "203.0.113.10"
    assert events[0].request_id == "hijack-20260807"
    assert events[1].ip_address is None
    assert events[1].request_id == ""
    assert str(events[0]) == "started: admin@example.test -> member@example.test"

    audit_admin = site._registry[AdminImpersonationAuditEvent]
    started_request.user = actor
    assert audit_admin.has_module_permission(started_request) is True
    assert audit_admin.has_view_permission(started_request, events[0]) is True
    assert audit_admin.has_add_permission(started_request) is False
    assert audit_admin.has_change_permission(started_request, events[0]) is False
    assert audit_admin.has_delete_permission(started_request, events[0]) is False
