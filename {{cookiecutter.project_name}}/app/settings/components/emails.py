from env import Env

from app.settings.components.aws import AWS_S3_REGION_NAME
from app.settings.vars import DOMAIN_NAME

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5
SERVER_EMAIL = Env.str(
    "SERVER_EMAIL",
    default=f"<system@{DOMAIN_NAME}>",
)
DEFAULT_FROM_EMAIL = Env.str(
    "DEFAULT_FROM_EMAIL",
    f"<no-reply@{DOMAIN_NAME}>",
)

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = Env.str(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = Env.str("EMAIL_HOST")
EMAIL_HOST_USER = Env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = Env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = Env.int("EMAIL_PORT")
EMAIL_USE_TLS = Env.bool("EMAIL_USE_TLS")

# Any Email
ANYMAIL = {"AMAZON_SES_CLIENT_PARAMS": {"region_name": AWS_S3_REGION_NAME}}

# Celery
CELERY_EMAIL_TASK_CONFIG = {
    "queue": "celery",
    # 'rate_limit' : '50/m',  # * CELERY_EMAIL_CHUNK_SIZE (default: 10) # noqa
}
