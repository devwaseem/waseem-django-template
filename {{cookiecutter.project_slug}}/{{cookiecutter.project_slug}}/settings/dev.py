"""Local-development settings with narrowly scoped convenience defaults."""

from copy import deepcopy
from typing import Any, cast
from urllib.parse import urlsplit

from .base import *  # noqa: F403


DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
INSTALLED_APPS += ["hyperdjango.integrations.devtools"]  # noqa: F405
MIDDLEWARE = [
    "hyperdjango.integrations.devtools.middleware.HyperDjangoDebugToolbarMiddleware",
    *MIDDLEWARE,  # noqa: F405
]
HYPER_DEBUG_TOOLBAR = True
HYPER_DEBUG_TOOLBAR_CONFIG = {
    "MAX_HISTORY": 50,
    "RECORD_PAGE_REQUESTS": False,
    "URL_PREFIX": "__hyperdebug__",
}
development_logging = cast(dict[str, Any], deepcopy(LOGGING))  # noqa: F405
logging_filters = cast(dict[str, Any], development_logging.get("filters", {}))
development_logging["filters"] = {
    **logging_filters,
    "skip_hyperdjango_request_inspector": {
        "()": "hyperdjango.integrations.devtools.logging.RequestInspectorAccessLogFilter"
    },
}
logging_handlers = cast(dict[str, Any], development_logging["handlers"])
console_handler = cast(dict[str, Any], logging_handlers["console"])
console_handler["filters"] = [
    *cast(list[str], console_handler.get("filters", [])),
    "skip_hyperdjango_request_inspector",
]
LOGGING = development_logging

CONTENT_SECURITY_POLICY = deepcopy(CONTENT_SECURITY_POLICY)  # noqa: F405
vite_url = urlsplit(HYPER_VITE_DEV_SERVER_URL)  # noqa: F405
vite_origin = f"{vite_url.scheme}://{vite_url.netloc}"
vite_websocket_scheme = "wss" if vite_url.scheme == "https" else "ws"
vite_websocket_origin = f"{vite_websocket_scheme}://{vite_url.netloc}"
CONTENT_SECURITY_POLICY["DIRECTIVES"]["script-src"].append(vite_origin)
CONTENT_SECURITY_POLICY["DIRECTIVES"]["style-src"].extend(
    [vite_origin, "'unsafe-inline'"]
)
CONTENT_SECURITY_POLICY["DIRECTIVES"]["connect-src"] = [
    "'self'",
    vite_origin,
    vite_websocket_origin,
]{% endif %}
