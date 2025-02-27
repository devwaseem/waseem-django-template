import os
from typing import Any

import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django.setup()

app = Celery("{{ cookiecutter.project_name }}")
app.config_from_object("app.celeryconfig")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **kwargs: Any) -> None:
    ...
