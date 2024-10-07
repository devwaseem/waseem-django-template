# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/
from app.settings.vars import NO_CACHE, REDIS_HOST, REDIS_PORT, TEST

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    },
}

if TEST:
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }

if NO_CACHE:
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
