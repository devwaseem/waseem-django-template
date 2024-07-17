from pathlib import Path

import environ

BASE_DIR = Path(__file__).parent

environ.Env.read_env(BASE_DIR / ".env")

Env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    TEST=(bool, False),
    ACCOUNT_ALLOW_REGISTRATION=(bool, True),
    REDIS_PORT=(int, 6379),
    MJML_PORT=(int, 28101),
    DJANGO_DATABASE_PORT=(int, 5432),
    CONN_MAX_AGE=(int, 60),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
    EMAIL_PORT=(int, 1025),
    EMAIL_USE_TLS=(bool, False),
    NO_CACHE=(bool, False),
    LOG_DB=(bool, False),
    DISABLE_LOGGING=(bool, False),
    ENABLE_HEALTH_CHECK=(bool, False),
    ENABLE_SILK_PROFILING=(bool, False),
    ENABLE_CPROFILE=(bool, False),
    ENABLE_PYINSTRUMENT=(bool, False),
    ENABLE_SENTRY=(bool, False),
    # security
    USE_SSL=(bool | None, None),
    USE_X_FORWARDED_HOST=(bool, False),
    # static
    STATIC_USE_WHITENOISE=(bool, False),
    DJANGO_STATIC_HOST=(str, ""),
    DJANGO_MEDIA_HOST=(str, ""),
    MEDIA_USE_S3=(bool, False),
    STATIC_USE_S3=(bool, False),
)
