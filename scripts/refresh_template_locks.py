"""Regenerate the lockfile for every supported Cookiecutter project shape."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from cookiecutter.main import cookiecutter

ROOT = Path(__file__).resolve().parents[1]
LOCKS = ROOT / "{{cookiecutter.project_slug}}" / ".template_locks"
PRESENTATION_TIMEZONE = "America/Toronto"
LOCKFILE_PROJECT_NAME = "{{ cookiecutter.project_slug | replace('_', '-') }}"


def refresh_lock(rendering_mode: str, enable_celery: str, output_dir: Path) -> None:
    """Render one shape, resolve it with uv, and preserve its lockfile."""
    project_slug = f"lock_{rendering_mode}_{enable_celery}"
    project = Path(
        cookiecutter(
            str(ROOT),
            no_input=True,
            output_dir=str(output_dir),
            extra_context={
                "project_name": f"Lock {rendering_mode} {enable_celery}",
                "project_slug": project_slug,
                "presentation_timezone": PRESENTATION_TIMEZONE,
                "license": "Proprietary",
                "rendering_mode": rendering_mode,
                "enable_celery": enable_celery,
            },
        )
    )
    subprocess.run(["uv", "lock"], cwd=project, check=True)
    destination = LOCKS / f"uv.{rendering_mode}.{enable_celery}.lock"
    shutil.copy2(project / "uv.lock", destination)
    parameterize_project_name(destination, project_slug)
    print(f"Refreshed {destination.relative_to(ROOT)}")


def parameterize_project_name(lockfile: Path, project_slug: str) -> None:
    """Keep the local package entry valid for every generated project slug."""
    content = lockfile.read_text(encoding="utf-8")
    normalized_project_name = project_slug.replace("_", "-")
    concrete_name = f'name = "{normalized_project_name}"'
    if content.count(concrete_name) != 1:
        raise RuntimeError(
            f"Expected exactly one local package entry named {project_slug!r} in "
            f"{lockfile}."
        )
    lockfile.write_text(
        content.replace(concrete_name, f'name = "{LOCKFILE_PROJECT_NAME}"'),
        encoding="utf-8",
    )


def main() -> None:
    """Refresh each generated project lockfile in isolation."""
    with tempfile.TemporaryDirectory(prefix="django-template-locks-") as temporary_dir:
        output_dir = Path(temporary_dir)
        for rendering_mode in ("api", "ssr", "hybrid"):
            for enable_celery in ("no", "yes"):
                refresh_lock(rendering_mode, enable_celery, output_dir)


if __name__ == "__main__":
    main()
