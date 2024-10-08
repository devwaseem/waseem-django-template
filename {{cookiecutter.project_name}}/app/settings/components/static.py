import re

from env import Env

from app.settings.components.common import MIDDLEWARE
from app.settings.components.storages import STORAGES
from app.settings.vars import BASE_DIR

STATIC_ROOT = STORAGES["staticfiles"]["OPTIONS"]["location"]  # type: ignore


STATICFILES_DIRS = [
    BASE_DIR / Env.str("VITE_APP_OUTPUT_DIR"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

if Env.bool("STATIC_USE_WHITENOISE"):
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

    def immutable_file_test(_: object, url: str) -> re.Match[str] | None:
        # Match filename with 12 hex digits before the extension
        # e.g. app.db8f2edc0c8a.js
        return re.match(r"^.+\.\w+\..+$", url)

    WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
