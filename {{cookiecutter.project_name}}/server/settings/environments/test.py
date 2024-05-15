from server.settings.components.database import DATABASES
from server.settings.environments.development import LOGGING  # type: ignore

LOGGING["loggers"]["django.db"] = {}  # type: ignore


DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}
