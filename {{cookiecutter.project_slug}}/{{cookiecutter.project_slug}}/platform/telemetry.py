"""Opt-in observability setup with privacy-preserving defaults."""

from __future__ import annotations

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import sentry_sdk

from {{ cookiecutter.project_slug }}.config.env import env


def initialize_telemetry() -> None:
    """Enable Sentry/OTEL only when operators explicitly configure them."""
    sentry_dsn = env.string("SENTRY_DSN", "")
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn, send_default_pii=False)

    endpoint = env.string("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    if not endpoint:
        return
    resource = Resource.create({SERVICE_NAME: env.string("OTEL_SERVICE_NAME")})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)
    DjangoInstrumentor().instrument()
    LoggingInstrumentor().instrument(set_logging_format=False)
