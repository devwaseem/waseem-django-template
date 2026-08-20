from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import Client, RequestFactory, override_settings

from {{ cookiecutter.project_slug }}.platform.logging import (
    add_trace_context,
    configure_logging,
    redact_sensitive_data,
)


def test_logging_and_opt_in_telemetry_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import {{ cookiecutter.project_slug }}.platform.logging as platform_logging
    import {{ cookiecutter.project_slug }}.platform.telemetry as telemetry

    configured = Mock()
    context = Mock()
    monkeypatch.setattr(platform_logging.structlog, "configure", configured)
    monkeypatch.setattr(platform_logging, "bind_contextvars", context)
    configure_logging(
        app_build_sha="build",
        app_version="1.2.3",
        debug=False,
        deployment_environment="test",
    )
    configure_logging(
        app_build_sha="build",
        app_version="1.2.3",
        debug=True,
        deployment_environment="test",
    )
    assert configured.call_count == 2
    context.assert_called_with(
        app_build_sha="build",
        app_version="1.2.3",
        deployment_environment="test",
    )

    monkeypatch.setattr(telemetry.env, "string", lambda _name, default="": default)
    telemetry.initialize_telemetry()

    configured_sentry = Mock()
    configured_provider = Mock()
    instrument = Mock()
    values = {
        "SENTRY_DSN": "dsn",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "https://otel.example.test",
        "OTEL_SERVICE_NAME": "service",
        "APP_VERSION": "1.2.3",
        "DEPLOYMENT_ENVIRONMENT": "test",
    }
    monkeypatch.setattr(
        telemetry.env, "string", lambda name, default="": values.get(name, default)
    )
    monkeypatch.setattr(telemetry.sentry_sdk, "init", configured_sentry)
    monkeypatch.setattr(telemetry.trace, "set_tracer_provider", configured_provider)
    monkeypatch.setattr(telemetry.DjangoInstrumentor, "instrument", instrument)
    monkeypatch.setattr(telemetry.LoggingInstrumentor, "instrument", instrument)
{% if cookiecutter.enable_celery == "yes" %}
    monkeypatch.setattr(telemetry.CeleryInstrumentor, "instrument", instrument)
{% endif %}
    telemetry.initialize_telemetry()
    configured_sentry.assert_called_once_with(
        before_send=telemetry.redact_sentry_event,
        dist="development",
        dsn="dsn",
        environment="test",
        release="service@1.2.3",
        send_default_pii=False,
        traces_sample_rate=0.0,
    )
    assert configured_provider.call_count == 1
    assert instrument.call_count == {% if cookiecutter.enable_celery == "yes" %}3{% else %}2{% endif %}


def test_observability_redacts_sentry_events_and_correlates_logs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import {{ cookiecutter.project_slug }}.platform.logging as platform_logging
    import {{ cookiecutter.project_slug }}.platform.telemetry as telemetry

    event = {
        "request": {
            "headers": {"authorization": "Bearer secret"},
            "data": {"password": "secret"},
        },
        "api_key": "secret",
    }
    assert telemetry.redact_sentry_event(event, None) == {
        "request": {"headers": "[REDACTED]", "data": "[REDACTED]"},
        "api_key": "[REDACTED]",
    }
    assert redact_sensitive_data(None, "info", {"client_secret": "secret"}) == {
        "client_secret": "[REDACTED]"
    }

    valid_context = SimpleNamespace(is_valid=True, trace_id=1, span_id=2)
    valid_span = Mock()
    valid_span.get_span_context.return_value = valid_context
    monkeypatch.setattr(platform_logging.trace, "get_current_span", lambda: valid_span)
    assert add_trace_context(None, "info", {}) == {
        "trace_id": "00000000000000000000000000000001",
        "span_id": "0000000000000002",
    }

    invalid_span = Mock()
    invalid_span.get_span_context.return_value = SimpleNamespace(is_valid=False)
    monkeypatch.setattr(
        platform_logging.trace, "get_current_span", lambda: invalid_span
    )
    assert add_trace_context(None, "info", {}) == {}


def test_trace_sampling_requires_a_probability(monkeypatch: pytest.MonkeyPatch) -> None:
    import {{ cookiecutter.project_slug }}.platform.telemetry as telemetry

    monkeypatch.setattr(telemetry.env, "string", lambda _name, _default="": "invalid")
    with pytest.raises(ImproperlyConfigured, match="OTEL_TRACE_SAMPLE_RATIO"):
        telemetry.trace_sample_ratio()

    monkeypatch.setattr(telemetry.env, "string", lambda _name, _default="": "1.1")
    with pytest.raises(ImproperlyConfigured, match="OTEL_TRACE_SAMPLE_RATIO"):
        telemetry.trace_sample_ratio()


def test_private_metrics_endpoint_and_http_metrics(
    client: Client,
    monkeypatch: pytest.MonkeyPatch,
    rf: RequestFactory,
) -> None:
    project_package = settings.ROOT_URLCONF.partition(".")[0]
    metrics = import_module(f"{project_package}.platform.metrics")
    counter = Mock()
    duration = Mock()
    monkeypatch.setattr(metrics, "HTTP_REQUESTS", counter)
    monkeypatch.setattr(metrics, "HTTP_REQUEST_DURATION", duration)
    request = rf.get("/orders/123/")
    request.resolver_match = SimpleNamespace(route="orders/<uuid:order_id>/")
    middleware = metrics.HttpMetricsMiddleware(
        lambda _request: HttpResponse(status=201)
    )

    metrics_token = "-".join(["metrics", "token"])
    with override_settings(METRICS_ENABLED=True, METRICS_TOKEN=metrics_token):
        assert middleware(request).status_code == 201
        counter.labels.assert_called_once_with(
            method="GET",
            route="orders/<uuid:order_id>/",
            status_code="201",
        )
        counter.labels.return_value.inc.assert_called_once_with()
        duration.labels.return_value.observe.assert_called_once()
        assert client.get("/metrics/").status_code == 403
        assert (
            client.get("/metrics/", HTTP_AUTHORIZATION="Bearer incorrect").status_code
            == 403
        )
        client.get("/version/")
        response = client.get("/metrics/", HTTP_AUTHORIZATION=f"Bearer {metrics_token}")
        assert response.status_code == 200
        assert b"http_server_requests_total" in response.content
        assert (
            client.post(
                "/metrics/", HTTP_AUTHORIZATION=f"Bearer {metrics_token}"
            ).status_code
            == 405
        )

    counter.reset_mock()
    with override_settings(METRICS_ENABLED=False):
        assert middleware(request).status_code == 201
        assert client.get("/metrics/").status_code == 404
    counter.labels.assert_not_called()


def test_metrics_ignore_probes_and_record_unhandled_errors(
    monkeypatch: pytest.MonkeyPatch,
    rf: RequestFactory,
) -> None:
    project_package = settings.ROOT_URLCONF.partition(".")[0]
    metrics = import_module(f"{project_package}.platform.metrics")
    counter = Mock()
    duration = Mock()
    monkeypatch.setattr(metrics, "HTTP_REQUESTS", counter)
    monkeypatch.setattr(metrics, "HTTP_REQUEST_DURATION", duration)
    probe = rf.get("/livez/")
    failing = rf.get("/missing/")
    failing.resolver_match = None

    def unavailable(_request: object) -> HttpResponse:
        raise RuntimeError("offline")

    with override_settings(METRICS_ENABLED=True):
        assert (
            metrics.HttpMetricsMiddleware(lambda _request: HttpResponse())(
                probe
            ).status_code
            == 200
        )
        with pytest.raises(RuntimeError, match="offline"):
            metrics.HttpMetricsMiddleware(unavailable)(failing)

    counter.labels.assert_called_once_with(
        method="GET", route="unmatched", status_code="500"
    )
    duration.labels.return_value.observe.assert_called_once()


def test_celery_propagates_and_clears_request_correlation() -> None:
    from types import SimpleNamespace

    from structlog.contextvars import (
        bind_contextvars,
        clear_contextvars,
        get_contextvars,
    )

    project_package = settings.ROOT_URLCONF.partition(".")[0]
    celery_module_name = f"{project_package}.platform.celery"
    if find_spec(celery_module_name) is None:
        return
    celery = import_module(celery_module_name)

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
