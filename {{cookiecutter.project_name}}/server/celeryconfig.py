from env import Env
from django.conf import settings

timezone = settings.TIME_ZONE
task_track_started = True
broker_url = Env("CELERY_BROKER_URL")
result_backend = "django-db"
cache_backend = "default"
celery_accept_content = ["application/json"]
task_serializer = "json"
result_serializer = "json"
imports = ("server.apps.main.tasks",)
broker_connection_retry_on_startup = True
