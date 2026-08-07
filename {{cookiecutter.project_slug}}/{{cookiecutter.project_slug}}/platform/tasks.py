"""Shared Celery task behavior for thin, idempotent domain adapters."""

from celery import Task


class DomainTask(Task):
    """Retry transient failures; task bodies should call a domain operation."""

    autoretry_for = (ConnectionError, TimeoutError)
    retry_backoff = True
    retry_jitter = True
    max_retries = 3
