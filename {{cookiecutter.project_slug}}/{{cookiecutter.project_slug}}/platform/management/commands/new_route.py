"""Create a complete HyperDjango page bundle for a server-rendered route."""

from __future__ import annotations

import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


VALID_ROUTE = re.compile(r"^[a-z][a-z0-9_/-]*$")


class Command(BaseCommand):
    help = "Create a HyperDjango route with page, template, and TypeScript entries."
    requires_system_checks: list[str] = []

    def add_arguments(self, parser: object) -> None:
        parser.add_argument("route")  # type: ignore[attr-defined]

    def handle(self, *args: object, **options: str) -> None:
        route = options["route"].strip("/")
        if not VALID_ROUTE.fullmatch(route) or "//" in route:
            raise CommandError("Use a route such as 'reports' or 'settings/profile'.")
        directory = Path(settings.BASE_DIR) / "hyper" / "routes" / route
        if directory.exists():
            raise CommandError(f"Route '{route}' already exists.")
        directory.mkdir(parents=True)
        title = route.rsplit("/", maxsplit=1)[-1].replace("_", " ").title()
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
                    f'    route_name = "{route.replace("/", "_")}"',
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
        self.stdout.write(self.style.SUCCESS(f"Created route '{route}'."))

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
