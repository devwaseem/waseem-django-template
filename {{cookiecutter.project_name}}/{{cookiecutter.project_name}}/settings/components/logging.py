# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/

# See also:
# 'Do not log' by Nikita Sobolev (@sobolevn)
# https://sobolevn.me/2020/03/do-not-log

from typing import TYPE_CHECKING

import structlog
from env import Env
from {{cookiecutter.project_name}}.settings.vars import DEBUG, TEST

if TYPE_CHECKING:
    from collections.abc import Callable
    from django.http import HttpRequest, HttpResponse

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # We use these formatters in our `'handlers'` configuration.
    # Probably, you won't need to modify these lines.
    # Unless, you know what you are doing.
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
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
            "formatter": "json_formatter",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_DJANGO"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "django_security_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_SECURITY"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_APP"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "celery_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_CELERY"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
    },
    # These loggers are required by our app:
    # - django is required when using `logger.getLogger('django')`
    # - security is required by `axes`
    "loggers": {
        "django.server": {
            "handlers": ["django_file", "mail_admins"],
            "propagate": True,
            "level": "INFO",
        },
        "django.security": {
            "handlers": ["django_security_file", "mail_admins"],
            "level": "WARNING",
            "propagate": True,
        },
        "celery": {
            "handlers": ["celery_file", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
        "{{cookiecutter.project_name}}": {
            "handlers": ["app_file", "mail_admins"],
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
        "django.db": {
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
        "{{cookiecutter.project_name}}": {
            "handlers": ["plain_console"],
            "level": "DEBUG",
            "propagate": True,
        },
    }

if TEST:
    LOGGING["loggers"]["django.db"] = {}  # type: ignore


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