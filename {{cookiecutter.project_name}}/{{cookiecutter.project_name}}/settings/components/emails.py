from env import Env
from {{cookiecutter.project_name}}.settings.components.aws import AWS_S3_REGION_NAME

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = Env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = Env("SERVER_EMAIL")

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = Env("EMAIL_BACKEND")
EMAIL_HOST = Env("EMAIL_HOST")
EMAIL_HOST_USER = Env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = Env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = Env("EMAIL_PORT")
EMAIL_USE_TLS = Env("EMAIL_USE_TLS", bool, default=False)

# Any Email
ANYMAIL = {"AMAZON_SES_CLIENT_PARAMS": {"region_name": AWS_S3_REGION_NAME}}

# Celery
CELERY_EMAIL_TASK_CONFIG = {
    "queue": "celery",
    # 'rate_limit' : '50/m',  # * CELERY_EMAIL_CHUNK_SIZE (default: 10) # noqa
}
