{% if cookiecutter.enable_celery == "yes" -%}
from __future__ import annotations


def test_celery_uses_a_conservative_default_queue() -> None:
    from {{ cookiecutter.project_slug }}.platform import celeryconfig

    assert celeryconfig.task_default_queue == "default"
    assert celeryconfig.task_acks_late is True
    assert celeryconfig.task_reject_on_worker_lost is True
    assert celeryconfig.worker_prefetch_multiplier == 1
    assert celeryconfig.beat_schedule == {}
{% endif -%}
