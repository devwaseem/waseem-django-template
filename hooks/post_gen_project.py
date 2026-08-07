"""Select feature layers and their lockfile without altering developer state."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
RENDERING_MODE = "{{ cookiecutter.rendering_mode }}"
ENABLE_CELERY = "{{ cookiecutter.enable_celery }}"


def remove(path: str) -> None:
    """Remove one generated path only when it is outside the selected shape."""
    target = ROOT / path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


lockfile = ROOT / ".template_locks" / f"uv.{RENDERING_MODE}.{ENABLE_CELERY}.lock"
shutil.copyfile(lockfile, ROOT / "uv.lock")
remove(".template_locks")

for path in (
    "env.py",
    "env_template.txt",
    "gunicorn_config.py",
    "observability",
    f"{PROJECT_SLUG}/platform/templates/email",
    ".vscode",
    "docs/deployment.md",
    "docs/observability.md",
    "docs/settings.md",
):
    remove(path)

if RENDERING_MODE == "api":
    for path in (
        "hyper",
        "package.json",
        "package-lock.json",
        "prettier.config.mjs",
        ".prettierignore",
        "tsconfig.json",
        "vite.config.ts",
        "playwright.config.ts",
        "tests/e2e",
        f"{PROJECT_SLUG}/platform/management/commands/new_route.py",
    ):
        remove(path)

if RENDERING_MODE == "ssr":
    remove(f"{PROJECT_SLUG}/api")

if ENABLE_CELERY == "no":
    for path in (
        f"{PROJECT_SLUG}/platform/celery.py",
        f"{PROJECT_SLUG}/platform/celeryconfig.py",
        f"{PROJECT_SLUG}/platform/tasks.py",
    ):
        remove(path)
