"""One conservative default queue and Beat configuration for product tasks."""

from {{ cookiecutter.project_slug }}.config.env import env


broker_url = env.string("CELERY_BROKER_URL")
result_backend = env.string("CELERY_RESULT_BACKEND")
task_default_queue = "default"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1
broker_connection_retry_on_startup = True
task_publish_retry = True
task_publish_retry_policy = {"max_retries": 3}
task_soft_time_limit = 270
task_time_limit = 300
task_track_started = True
timezone = "UTC"
beat_schedule: dict[str, object] = {}
