# https://github.com/revsys/django-health-check

from app.settings.components.caches import CACHES
from app.settings.components.common import INSTALLED_APPS
from app.settings.vars import REDIS_HOST, REDIS_PORT

INSTALLED_APPS += [
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",  # requires celery
    "health_check.contrib.celery_ping",  # requires celery
    "health_check.contrib.psutil",  # disk and memory utilization; requires psutil # noqa
    "health_check.contrib.s3boto3_storage",  # requires boto3 and S3BotoStorage backend # noqa
    # "health_check.contrib.rabbitmq",  # requires RabbitMQ broker
    "health_check.contrib.redis",  # requires Redis broker
]

HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,  # percent
    "MEMORY_MIN": 100,  # in MB
}

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

HEALTHCHECK_CACHE_KEY = "health_check"

CACHES[HEALTHCHECK_CACHE_KEY] = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/3",
}
