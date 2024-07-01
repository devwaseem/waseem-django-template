import os

import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

django.setup()

app = Celery("{{ cookiecutter.project_name }}")
app.config_from_object("src.celeryconfig")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "Backup Database": {
        "task": "backup_db",
        "schedule": crontab(
            minute="0", hour="1", day_of_week="0"
        ),  # run every sundays at 1:00 AM
    },
}
