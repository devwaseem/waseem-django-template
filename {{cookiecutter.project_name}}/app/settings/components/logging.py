# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/

# See also:
# 'Do not log' by Nikita Sobolev (@sobolevn)
# https://sobolevn.me/2020/03/do-not-log

from typing import TYPE_CHECKING

import structlog
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django_structlog import signals
from env import Env

from app.settings.vars import DEBUG

if TYPE_CHECKING:
    from collections.abc import Callable

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # We use these formatters in our `'handlers'` configuration.
    # Probably, you won't need to modify these lines.
    # Unless, you know what you are doing.
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.ExceptionPrettyPrinter(),
            ],
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"],
            ),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                # customize the rest as you need
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.ExceptionPrettyPrinter(),
            ],
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                # customize the rest as you need
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.ExceptionPrettyPrinter(),
            ],
        },
    },
    # You can easily swap `key/value` (default) output and `json` ones.
    # Use `'json_console'` if you need `json` logs.
    "handlers": {
        "plain_console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    # These loggers are required by our app:
    # - django is required when using `logger.getLogger('django')`
    # - security is required by `axes`
    "loggers": {
        "django_structlog": {
            "handlers": ["json_console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.server": {
            "handlers": ["json_console", "mail_admins"],
            "propagate": True,
            "level": "INFO",
        },
        "django.security": {
            "handlers": ["json_console", "mail_admins"],
            "level": "WARNING",
            "propagate": True,
        },
        "celery": {
            "handlers": ["json_console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
        "app": {
            "handlers": ["json_console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

if DEBUG:
    LOGGING["handlers"] = {
        "plain_console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    }
    LOGGING["loggers"] = {
        "django_structlog": {
            "handlers": ["plain_console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "werkzeug": {
            "handlers": ["plain_console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["plain_console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "django.server": {
            "handlers": ["plain_console"],
            "propagate": False,
            "level": "DEBUG",
        },
        "django.core.cache": {
            "handlers": ["plain_console"],
            "propagate": False,
            "level": "DEBUG",
        },
        "django.template": {
            "handlers": ["plain_console"],
            "propagate": False,
            "level": "DEBUG",
        },
        "django.security": {
            "handlers": ["plain_console"],
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": ["plain_console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["plain_console"],
            "level": "DEBUG",
            "propagate": True,
        },
    }
    if Env.bool("LOG_DB"):
        LOGGING["loggers"]["django.db"] = {  # type: ignore
            "handlers": ["plain_console"],
            "propagate": False,
            "level": "DEBUG",
        }

if Env.bool("DISABLE_LOGGING"):
    LOGGING["loggers"] = {}


class LoggingContextVarsMiddleware:
    """Used to reset ContextVars in structlog on each request."""

    def __init__(
        self,
        get_response: "Callable[[HttpRequest], HttpResponse]",
    ) -> None:
        """Django's API-compatible constructor."""
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        """
        Handle requests.

        Add your logging metadata here.
        Example: https://github.com/jrobichaud/django-structlog
        """
        response = self.get_response(request)
        structlog.contextvars.clear_contextvars()
        return response


if not structlog.is_configured():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


@receiver(signals.bind_extra_request_metadata)
def bind_domain(request: HttpRequest, logger: Any, **_kwargs: Any) -> None:  # type: ignore # noqa
    current_site = get_current_site(request)
    structlog.contextvars.bind_contextvars(domain=current_site.domain)
