"""Run Uvicorn directly with typed, environment-controlled settings."""

from __future__ import annotations

import uvicorn

from {{ cookiecutter.project_slug }}.config.env import env


def main() -> None:
    """Start the ASGI application without a Gunicorn wrapper."""
    uvicorn.run(
        "{{ cookiecutter.project_slug }}.asgi:application",
        host=env.string("UVICORN_HOST", "0.0.0.0"),  # nosec B104
        port=env.integer("UVICORN_PORT", 8000),
        workers=env.integer("UVICORN_WORKERS", 1),
        timeout_keep_alive=env.integer("UVICORN_TIMEOUT_KEEP_ALIVE", 5),
        timeout_graceful_shutdown=env.integer("UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN", 30),
        proxy_headers=True,
        forwarded_allow_ips=env.string("UVICORN_FORWARDED_ALLOW_IPS", "127.0.0.1"),
        log_config=None,
    )


if __name__ == "__main__":
    main()
