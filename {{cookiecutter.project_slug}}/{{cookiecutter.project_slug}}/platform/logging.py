"""Structured logging helpers with deliberate redaction boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from opentelemetry import trace
import structlog
from structlog.contextvars import bind_contextvars


SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "api-key",
        "api_key",
        "access_token",
        "cookie",
        "client_secret",
        "csrfmiddlewaretoken",
        "data",
        "headers",
        "query_string",
        "request_body",
        "request_data",
        "set-cookie",
        "set_cookie",
        "password",
        "password1",
        "password2",
        "refresh",
        "secret",
        "token",
    }
)
SENSITIVE_KEY_FRAGMENTS = frozenset(
    {"authorization", "cookie", "credential", "password", "secret", "token"}
)
REDACTED = "[REDACTED]"


def is_sensitive_key(key: object) -> bool:
    """Recognize exact and composite secret-bearing field names safely."""
    if not isinstance(key, str):
        return False
    normalized_key = key.lower()
    return normalized_key in SENSITIVE_KEYS or any(
        fragment in normalized_key for fragment in SENSITIVE_KEY_FRAGMENTS
    )


def redact_sensitive_data(
    _logger: Any,
    _method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Redact known secret keys recursively before an event reaches a sink."""

    def scrub(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {
                key: REDACTED if is_sensitive_key(key) else scrub(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [scrub(item) for item in value]
        if isinstance(value, tuple):
            return tuple(scrub(item) for item in value)
        return value

    return scrub(event_dict)


def add_trace_context(
    _logger: Any,
    _method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Attach a valid active trace identity without recording request data."""
    span_context = trace.get_current_span().get_span_context()
    if span_context.is_valid:
        event_dict["trace_id"] = f"{span_context.trace_id:032x}"
        event_dict["span_id"] = f"{span_context.span_id:016x}"
    return event_dict


def configure_logging(
    *,
    app_build_sha: str,
    app_version: str,
    debug: bool,
    deployment_environment: str,
) -> None:
    """Configure JSON logs without request bodies, tokens, or auth cookies."""
    bind_contextvars(
        app_build_sha=app_build_sha,
        app_version=app_version,
        deployment_environment=deployment_environment,
    )
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        add_trace_context,
        redact_sensitive_data,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if debug:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
