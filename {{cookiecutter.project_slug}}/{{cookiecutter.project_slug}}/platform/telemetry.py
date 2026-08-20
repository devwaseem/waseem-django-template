"""Opt-in observability setup with privacy-preserving defaults."""

from __future__ import annotations

from typing import Any

from django.core.exceptions import ImproperlyConfigured
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
{% if cookiecutter.enable_celery == "yes" %}
from opentelemetry.instrumentation.celery import CeleryInstrumentor
{% endif %}
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import sentry_sdk

from {{ cookiecutter.project_slug }}.config.env import env
from {{ cookiecutter.project_slug }}.platform.logging import redact_sensitive_data


def redact_sentry_event(event: dict[str, Any], _hint: Any) -> dict[str, Any]:
    """Apply the same redaction policy before Sentry receives an event."""
    return redact_sensitive_data(None, "error", event)


def trace_sample_ratio() -> float:
    """Read a bounded head-sampling rate before trace export starts."""
    value = env.string("OTEL_TRACE_SAMPLE_RATIO", "0.1")
    try:
        ratio = float(value)
    except ValueError as error:
        message = "OTEL_TRACE_SAMPLE_RATIO must be a number from 0 through 1."
        raise ImproperlyConfigured(message) from error
    if not 0 <= ratio <= 1:
        raise ImproperlyConfigured(
            "OTEL_TRACE_SAMPLE_RATIO must be a number from 0 through 1."
        )
    return ratio


def telemetry_resource() -> Resource:
    """Describe a release consistently across traces and error reporting."""
    return Resource.create(
        {
            SERVICE_NAME: env.string("OTEL_SERVICE_NAME"),
            "service.version": env.string("APP_VERSION", "0.1.0"),
            "vcs.ref.head.revision": env.string("APP_BUILD_SHA", "development"),
            "deployment.environment.name": env.string(
                "DEPLOYMENT_ENVIRONMENT", "development"
            ),
        }
    )


def initialize_telemetry() -> None:
    """Enable opt-in error reporting and sampled HTTP/task traces."""
    sentry_dsn = env.string("SENTRY_DSN", "")
    if sentry_dsn:
        sentry_sdk.init(
            before_send=redact_sentry_event,
            dist=env.string("APP_BUILD_SHA", "development"),
            dsn=sentry_dsn,
            environment=env.string("DEPLOYMENT_ENVIRONMENT", "development"),
            release=(
                f"{env.string('OTEL_SERVICE_NAME')}@"
                f"{env.string('APP_VERSION', '0.1.0')}"
            ),
            send_default_pii=False,
            traces_sample_rate=0.0,
        )

    endpoint = env.string("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    if not endpoint:
        return
    provider = TracerProvider(
        resource=telemetry_resource(),
        sampler=ParentBased(TraceIdRatioBased(trace_sample_ratio())),
    )
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)
    DjangoInstrumentor().instrument(excluded_urls="livez,readyz,metrics")
    LoggingInstrumentor().instrument(set_logging_format=False)
{% if cookiecutter.enable_celery == "yes" %}
    CeleryInstrumentor().instrument()
{% endif -%}
