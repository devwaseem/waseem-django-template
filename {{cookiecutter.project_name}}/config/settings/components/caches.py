import os

# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/


REDIS_HOST = os.environ.get("REDIS_HOST")

CACHES = {
    "default": {
        # like https://github.com/jazzband/django-redis
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379",
    },
}
