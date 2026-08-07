"""Shared Celery task behavior for thin, idempotent domain adapters."""

from celery import Task


class DomainTask(Task):
    """Retry bounded transient failures; task bodies call idempotent operations."""

    autoretry_for = (ConnectionError, TimeoutError)
    retry_backoff = True
    retry_backoff_max = 300
    retry_jitter = True
    max_retries = 3
