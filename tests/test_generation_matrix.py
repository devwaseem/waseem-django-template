from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

ROOT = Path(__file__).resolve().parents[1]


def render_project(tmp_path: Path, *, rendering_mode: str, enable_celery: str) -> Path:
    slug = f"sample_{rendering_mode}_{enable_celery}"
    output = cookiecutter(
        str(ROOT),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={
            "project_name": f"Sample {rendering_mode} {enable_celery}",
            "project_slug": slug,
            "rendering_mode": rendering_mode,
            "enable_celery": enable_celery,
        },
    )
    return Path(output)


@pytest.mark.template
@pytest.mark.parametrize("rendering_mode", ["api", "ssr", "hybrid"])
@pytest.mark.parametrize("enable_celery", ["no", "yes"])
def test_every_supported_shape_renders_with_its_expected_layers(
    tmp_path: Path, rendering_mode: str, enable_celery: str
) -> None:
    project = render_project(
        tmp_path, rendering_mode=rendering_mode, enable_celery=enable_celery
    )
    slug = project.name

    assert (project / "uv.lock").is_file()
    assert not (project / ".template_locks").exists()
    assert not (project / ".pytest_cache").exists()
    assert not (project / ".ruff_cache").exists()
    assert not (project / "node_modules").exists()
    assert (project / slug / "platform" / "models.py").is_file()
    assert (project / slug / "platform" / "request_id.py").is_file()
    assert (
        project / slug / "platform" / "management" / "commands" / "doctor.py"
    ).is_file()
    assert (project / "tests" / "test_production_settings.py").is_file()
    assert (project / "AGENTS.md").is_file()
    assert (project / "compose.yaml").is_file()
    assert (project / slug / "platform" / "celery.py").exists() is (
        enable_celery == "yes"
    )
    assert (project / slug / "api").exists() is (rendering_mode != "ssr")
    assert (project / "hyper").exists() is (rendering_mode != "api")
    assert (project / "package-lock.json").exists() is (rendering_mode != "api")
    assert (project / ".github" / "workflows" / "publish-image.yml").is_file()
    assert (project / ".github" / "workflows" / "release-provenance.yml").is_file()
    assert (project / "docs" / "configuration.md").is_file()
    justfile = (project / "justfile").read_text(encoding="utf-8")
    assert "verify:" in justfile
    assert "Frontend checks: skipped (API mode has no frontend layer)" in justfile
    assert "Pre-commit: skipped (initialize Git to enable repository checks)" in justfile


def generated_environment(slug: str) -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "DJANGO_SETTINGS_MODULE": f"{slug}.settings.dev",
            "DEBUG": "false",
            "SECRET_KEY": "template-contract-secret-key-that-is-long-and-not-used",
            "ALLOWED_HOSTS": "localhost",
            "POSTGRES_DB": slug,
            "POSTGRES_USER": slug,
            "POSTGRES_PASSWORD": slug,
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "REDIS_URL": "redis://127.0.0.1:6379/0",
            "STATIC_USE_S3": "false",
            "MEDIA_USE_S3": "false",
        }
    )
    return environment


def run_generated_command(project: Path, *arguments: str) -> None:
    result = subprocess.run(
        [
            "uv",
            "run",
            "--directory",
            str(project),
            "--frozen",
            "python",
            "manage.py",
            *arguments,
        ],
        cwd=project,
        env=generated_environment(project.name),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.template_integration
@pytest.mark.parametrize("rendering_mode", ["api", "ssr", "hybrid"])
def test_generated_scaffolds_respect_the_selected_project_shape(
    tmp_path: Path, rendering_mode: str
) -> None:
    project = render_project(
        tmp_path, rendering_mode=rendering_mode, enable_celery="no"
    )
    slug = project.name

    run_generated_command(project, "new_domain", "billing")
    domain = project / slug / "domains" / "billing"
    assert (domain / "operations.py").is_file()
    assert (domain / "tests" / "test_operations.py").is_file()
    assert (domain / "api.py").exists() is (rendering_mode != "ssr")
    assert (project / "hyper" / "routes" / "billing").exists() is (
        rendering_mode != "api"
    )

    if rendering_mode != "api":
        run_generated_command(project, "new_route", "reports/status")
        route = project / "hyper" / "routes" / "reports" / "status"
        assert (route / "+page.py").is_file()
        assert (route / "entry.ts").is_file()
        assert (route / "entry.head.ts").is_file()


def run(command: list[str], *, cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.template_upgrade
def test_cruft_update_preserves_product_extensions(tmp_path: Path) -> None:
    template = tmp_path / "template"
    project_parent = tmp_path / "projects"
    shutil.copytree(
        ROOT,
        template,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
            ".ruff_cache",
            "__pycache__",
        ),
    )
    marker = template / "{{cookiecutter.project_slug}}" / "docs" / "upgrade-contract.md"
    marker.write_text("template revision one\n", encoding="utf-8")
    run(["git", "init"], cwd=template)
    run(["git", "config", "user.email", "template@example.test"], cwd=template)
    run(["git", "config", "user.name", "Template Test"], cwd=template)
    run(["git", "add", "."], cwd=template)
    run(["git", "commit", "-m", "template revision one"], cwd=template)

    run(
        [
            sys.executable,
            "-m",
            "cruft",
            "create",
            str(template),
            "--no-input",
            "--output-dir",
            str(project_parent),
        ],
        cwd=tmp_path,
    )
    project = project_parent / "acme_portal"
    run(["git", "init"], cwd=project)
    run(["git", "config", "user.email", "consumer@example.test"], cwd=project)
    run(["git", "config", "user.name", "Consumer Test"], cwd=project)
    run(["git", "add", "."], cwd=project)
    run(["git", "commit", "-m", "generated project"], cwd=project)

    product_file = project / "acme_portal" / "domains" / "inventory" / "operations.py"
    product_file.parent.mkdir(parents=True)
    product_file.write_text(
        '"""Product-owned inventory behavior."""\n', encoding="utf-8"
    )
    marker.write_text("template revision two\n", encoding="utf-8")
    run(["git", "add", "."], cwd=template)
    run(["git", "commit", "-m", "template revision two"], cwd=template)

    run(
        [
            sys.executable,
            "-m",
            "cruft",
            "update",
            "--project-dir",
            str(project),
            "--template-path",
            str(template),
            "--skip-apply-ask",
            "--allow-untracked-files",
        ],
        cwd=tmp_path,
    )

    assert (project / "docs" / "upgrade-contract.md").read_text(encoding="utf-8") == (
        "template revision two\n"
    )
    assert product_file.read_text(encoding="utf-8") == (
        '"""Product-owned inventory behavior."""\n'
    )
