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
    NO_CACHE=(bool, False),
    LOG_DB=(bool, False),
    ENABLE_HEALTH_CHECK=(bool, False),
    ENABLE_SILK_PROFILING=(bool, False),
    ENABLE_CPROFILE=(bool, False),
    ENABLE_PYINSTRUMENT=(bool, False),
    ENABLE_SENTRY=(bool, False),
)
