"""Configuration and public-contract assertions for generated projects."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "{{ cookiecutter.project_slug }}"
CONFIGURATION_DOCUMENT = PROJECT_ROOT / "docs" / "configuration.md"
EXAMPLE_ENVIRONMENT = PROJECT_ROOT / ".env.example"
ENVIRONMENT_READ = re.compile(
    r'env\.(?:string|integer|number|boolean|list)\(\s*"([A-Z][A-Z0-9_]*)"'
)
DIRECT_ENVIRONMENT_READ = re.compile(
    r'os\.environ\.(?:get|setdefault)\(\s*"([A-Z][A-Z0-9_]*)"'
)
COMPOSE_ENVIRONMENT_READ = re.compile(r"\$\{([A-Z][A-Z0-9_]*)")
DOCUMENTED_VARIABLE = re.compile(r"^\|\s*`([A-Z][A-Z0-9_]*)`\s*\|", re.MULTILINE)


SECURITY_SETTINGS = {
    "CONTENT_SECURITY_POLICY",
    "SESSION_COOKIE_SECURE",
    "CSRF_COOKIE_SECURE",
    "CORS_ALLOW_ALL_ORIGINS",
    "CORS_ALLOWED_ORIGINS",
    "STORAGES",
    "LOGGING",
    "RATELIMIT_ENABLE",
    "RATELIMIT_USE_CACHE",
    "RATELIMIT_FAIL_OPEN",
    "METRICS_ENABLED",
    "METRICS_TOKEN",
}


def environment_example_variables() -> set[str]:
    return {
        line.partition("=")[0]
        for line in EXAMPLE_ENVIRONMENT.read_text(encoding="utf-8").splitlines()
        if "=" in line and not line.lstrip().startswith("#")
    }


def runtime_environment_variables() -> set[str]:
    runtime_files = [*PACKAGE_ROOT.rglob("*.py"), PROJECT_ROOT / "manage.py"]
    source = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    compose_source = (PROJECT_ROOT / "compose.yaml").read_text(encoding="utf-8")
    return {
        *ENVIRONMENT_READ.findall(source),
        *DIRECT_ENVIRONMENT_READ.findall(source),
        *COMPOSE_ENVIRONMENT_READ.findall(compose_source),
    }


def documented_environment_variables() -> set[str]:
    return set(
        DOCUMENTED_VARIABLE.findall(CONFIGURATION_DOCUMENT.read_text(encoding="utf-8"))
    )


def deprecated_environment_variables() -> set[str]:
    document = CONFIGURATION_DOCUMENT.read_text(encoding="utf-8")
    _heading, _separator, deprecated_section = document.partition(
        "## Deprecated environment variables"
    )
    return set(DOCUMENTED_VARIABLE.findall(deprecated_section))


def test_environment_documentation_and_runtime_are_in_lockstep() -> None:
    example = environment_example_variables()
    documented = documented_environment_variables()
    runtime = runtime_environment_variables()
    deprecated = deprecated_environment_variables()

    assert example == documented
    assert documented <= runtime | deprecated
    assert runtime <= documented


def test_critical_runtime_security_settings_are_documented() -> None:
    documentation = CONFIGURATION_DOCUMENT.read_text(encoding="utf-8")

    for setting in SECURITY_SETTINGS:
        assert f"`{setting}`" in documentation
