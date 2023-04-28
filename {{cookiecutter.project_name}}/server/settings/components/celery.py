from server.settings import env

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND"
)
CELERY_IMPORTS = ("server.apps.main.tasks",)
