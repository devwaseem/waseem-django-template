import os

from server.settings.components.common import INSTALLED_APPS

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

INSTALLED_APPS += ["storages"]

BASE_URL = os.environ.get("DOMAIN_NAME")

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="").split()
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
# SECURE_HSTS_SECONDS = 86400  # 1 day
SECURE_HSTS_SECONDS = 300  # 5 Minutes
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default="").split()

STATIC_ROOT = "/var/www/static"

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = True
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "media"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_HOST = f"{AWS_S3_REGION_NAME}.amazonaws.com"

ANYMAIL = {"AMAZON_SES_CLIENT_PARAMS": {"region_name": AWS_S3_REGION_NAME}}

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

# Django Vite
DJANGO_VITE_DEV_MODE = False
