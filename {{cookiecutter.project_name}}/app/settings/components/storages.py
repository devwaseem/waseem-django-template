from env import Env

from app.settings.components.aws import AWS_S3_CUSTOM_DOMAIN
from app.settings.vars import DEBUG

DJANGO_STATIC_HOST = Env.str("DJANGO_STATIC_HOST")
DJANGO_MEDIA_HOST = Env.str("DJANGO_MEDIA_HOST")

MEDIA_LOCATION = "media"
STATIC_LOCATION = "static" if DEBUG else "/var/www/static"

MEDIA_URL = f"{DJANGO_MEDIA_HOST}/media/"
STATIC_URL = f"{DJANGO_STATIC_HOST}/static/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_LOCATION,
            "base_url": MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",  # noqa
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": STATIC_URL,
        },
    },
}


if Env.bool("MEDIA_USE_S3"):
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STORAGES["default"] = {
        "BACKEND": "app.settings.components.aws.PublicMediaStorage",
        "OPTIONS": {
            "location": MEDIA_LOCATION,
        },
    }

if Env.bool("STATIC_USE_S3"):
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    STORAGES["staticfiles"] = {
        "BACKEND": "app.settings.components.aws.StaticStorage",
        "OPTIONS": {
            "location": STATIC_LOCATION,
        },
    }

if Env.bool("STATIC_USE_WHITENOISE"):
    STATIC_URL = f"{DJANGO_STATIC_HOST}/static/"
    STORAGES["staticfiles"] = {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": STATIC_URL,
        },
    }
