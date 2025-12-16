import logging.config
import os
from typing import Any

import django
from celery import Celery, signals
from django.conf import settings
from django_structlog.celery.steps import DjangoStructLogInitStep

Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore[attr-defined] # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django.setup()

app = Celery("{{ cookiecutter.project_name }}")
app.config_from_object("app.celeryconfig")

app.steps["worker"].add(DjangoStructLogInitStep)

packages = [
    "app.tasks",
]

app.autodiscover_tasks(packages=packages)


@signals.setup_logging.connect
def setup_celery_logging(**_kwargs: Any) -> None:
    logging.config.dictConfig(settings.LOGGING)


@app.on_after_configure.connect
def setup_periodic_tasks(_sender: Any, **_kwargs: Any) -> None:
    ...
