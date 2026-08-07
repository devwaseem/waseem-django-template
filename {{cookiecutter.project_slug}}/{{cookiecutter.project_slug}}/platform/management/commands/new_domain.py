"""Create the consistent initial shape for a product domain."""

from __future__ import annotations

import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


VALID_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


class Command(BaseCommand):
    help = "Create a product domain with operations, models, tests, and transports."
    requires_system_checks: list[str] = []

    def add_arguments(self, parser: object) -> None:
        parser.add_argument("name")  # type: ignore[attr-defined]

    def handle(self, *args: object, **options: str) -> None:
        name = options["name"]
        if not VALID_NAME.fullmatch(name):
            raise CommandError(
                "Use a lowercase Python identifier, for example 'billing'."
            )

        project_package = settings.ROOT_URLCONF.partition(".")[0]
        directory = Path(settings.BASE_DIR) / project_package / "domains" / name
        if directory.exists():
            raise CommandError(f"Domain '{name}' already exists.")
        directory.mkdir(parents=True)
        self._write(directory / "__init__.py", "")
        self._write(
            directory / "apps.py",
            "\n".join(
                [
                    "from django.apps import AppConfig",
                    "",
                    "",
                    "class DomainConfig(AppConfig):",
                    f'    name = "{project_package}.domains.{name}"',
                    f'    label = "{name}"',
                    "",
                ]
            ),
        )
        self._write(
            directory / "models.py", '"""Domain persistence and invariants."""\n'
        )
        self._write(directory / "operations.py", '"""Domain business use cases."""\n')
        tests = directory / "tests"
        tests.mkdir()
        self._write(tests / "__init__.py", "")
        self._write(tests / "test_operations.py", '"""Domain operation tests."""\n')

        if settings.RENDERING_MODE != "ssr":
            self._write(
                directory / "api.py",
                "\n".join(
                    [
                        '"""Explicit API transport for this domain."""',
                        "",
                        "from ninja import Router",
                        "",
                        f'router = Router(tags=["{name.replace("_", " ").title()}"])',
                        "",
                    ]
                ),
            )
        if settings.RENDERING_MODE != "api":
            self._write_ssr_route(name)

        self.stdout.write(self.style.SUCCESS(f"Created domain '{name}'."))
        self.stdout.write(
            self.style.WARNING(
                "Register the app and its optional API/navigation extension in domains/registry.py."
            )
        )

    def _write_ssr_route(self, name: str) -> None:
        directory = Path(settings.BASE_DIR) / "hyper" / "routes" / name
        directory.mkdir(parents=True, exist_ok=False)
        title = name.replace("_", " ").title()
        self._write(
            directory / "+page.py",
            "\n".join(
                [
                    "from django.http import HttpRequest, HttpResponse",
                    "",
                    "from hyper.layouts.base import BaseLayout",
                    "",
                    "",
                    "class PageView(BaseLayout):",
                    f'    route_name = "{name}"',
                    "",
                    "    def __init__(self) -> None:",
                    f'        super().__init__(title="{title}")',
                    "",
                    "    def get(self, request: HttpRequest) -> HttpResponse:",
                    "        return HttpResponse(self.render(request=request))",
                    "",
                ]
            ),
        )
        self._write(
            directory / "index.html",
            "\n".join(
                [
                    "{{ '{%' }} extends 'layouts/dashboard/index.html' %}",
                    "{{ '{%' }} block dashboard_content %}",
                    f"<main><h1>{title}</h1></main>",
                    "{{ '{%' }} endblock %}",
                    "",
                ]
            ),
        )
        self._write(directory / "entry.ts", "export {};\n")
        self._write(directory / "entry.head.ts", "export {};\n")

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
