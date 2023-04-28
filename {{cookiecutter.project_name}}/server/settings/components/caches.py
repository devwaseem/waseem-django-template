from server.settings import env

# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/


DJANGO_CACHE_REDIS_URL = env("DJANGO_CACHE_REDIS_URL")


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{DJANGO_CACHE_REDIS_URL}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    },
}
