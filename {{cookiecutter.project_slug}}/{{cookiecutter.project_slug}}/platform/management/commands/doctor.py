"""Read-only local diagnostics for the generated application."""

from __future__ import annotations

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "Check configuration plus PostgreSQL and Redis connectivity without writes."
    requires_system_checks: list[str] = []

    def handle(self, *args: object, **options: object) -> None:
        checks = (
            ("PostgreSQL", self._check_database),
            ("Redis", self._check_cache),
        )
        failures: list[str] = []
        for name, check in checks:
            try:
                check()
            except Exception as error:
                failures.append(f"{name}: {error}")
            else:
                self.stdout.write(self.style.SUCCESS(f"{name}: ok"))

        self.stdout.write(f"Rendering mode: {settings.RENDERING_MODE}")
        if failures:
            raise CommandError(
                "Doctor found unavailable dependencies: " + "; ".join(failures)
            )
        self.stdout.write(self.style.SUCCESS("Application diagnostics: ok"))

    @staticmethod
    def _check_database() -> None:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")

    @staticmethod
    def _check_cache() -> None:
        cache.get("platform:doctor")
