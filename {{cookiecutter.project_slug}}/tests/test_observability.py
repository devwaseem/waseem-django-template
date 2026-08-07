from __future__ import annotations

from unittest.mock import Mock

import pytest

from {{ cookiecutter.project_slug }}.platform.logging import configure_logging


def test_logging_and_opt_in_telemetry_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import {{ cookiecutter.project_slug }}.platform.logging as platform_logging
    import {{ cookiecutter.project_slug }}.platform.telemetry as telemetry

    configured = Mock()
    monkeypatch.setattr(platform_logging.structlog, "configure", configured)
    configure_logging(debug=False)
    configure_logging(debug=True)
    assert configured.call_count == 2

    monkeypatch.setattr(telemetry.env, "string", lambda _name, default="": default)
    telemetry.initialize_telemetry()

    configured_sentry = Mock()
    configured_provider = Mock()
    instrument = Mock()
    values = {
        "SENTRY_DSN": "dsn",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.example.test",
        "OTEL_SERVICE_NAME": "service",
    }
    monkeypatch.setattr(
        telemetry.env, "string", lambda name, default="": values.get(name, default)
    )
    monkeypatch.setattr(telemetry.sentry_sdk, "init", configured_sentry)
    monkeypatch.setattr(telemetry.trace, "set_tracer_provider", configured_provider)
    monkeypatch.setattr(telemetry.DjangoInstrumentor, "instrument", instrument)
    monkeypatch.setattr(telemetry.LoggingInstrumentor, "instrument", instrument)
    telemetry.initialize_telemetry()
    assert configured_sentry.called
    assert configured_provider.called
    assert instrument.call_count == 2


{% if cookiecutter.enable_celery == "yes" -%}
def test_celery_propagates_and_clears_request_correlation() -> None:
    from types import SimpleNamespace

    from structlog.contextvars import (
        bind_contextvars,
        clear_contextvars,
        get_contextvars,
    )

    from {{ cookiecutter.project_slug }}.platform import celery

    clear_contextvars()
    headers: dict[str, str] = {}
    celery.attach_request_id(headers)
    assert headers == {}
    celery.attach_request_id(None)

    bind_contextvars(request_id="request-12345678")
    celery.attach_request_id(headers)
    assert headers == {"x-request-id": "request-12345678"}
    clear_contextvars()
    fake_task = SimpleNamespace(
        request=SimpleNamespace(headers={"x-request-id": "request-12345678"})
    )
    celery.bind_task_context("task-123", fake_task)
    assert get_contextvars()["request_id"] == "request-12345678"
    assert get_contextvars()["task_id"] == "task-123"
    celery.clear_task_context("task-123")
    assert get_contextvars() == {}
    invalid_task = SimpleNamespace(
        request=SimpleNamespace(headers={"x-request-id": "invalid"})
    )
    celery.bind_task_context("task-invalid", invalid_task)
    assert get_contextvars() == {"task_id": "task-invalid"}
    celery.clear_task_context("task-invalid")
    celery.clear_task_context("missing-task")
{% endif -%}
