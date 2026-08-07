"""Structured logging helpers with deliberate redaction boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import structlog


SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "cookie",
        "csrfmiddlewaretoken",
        "password",
        "password1",
        "password2",
        "refresh",
        "secret",
        "token",
    }
)
REDACTED = "[REDACTED]"


def redact_sensitive_data(
    _logger: Any,
    _method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Redact known secret keys recursively before an event reaches a sink."""

    def scrub(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {
                key: REDACTED if key.lower() in SENSITIVE_KEYS else scrub(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [scrub(item) for item in value]
        if isinstance(value, tuple):
            return tuple(scrub(item) for item in value)
        return value

    return scrub(event_dict)


def configure_logging(*, debug: bool) -> None:
    """Configure JSON logs without request bodies, tokens, or auth cookies."""
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
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
