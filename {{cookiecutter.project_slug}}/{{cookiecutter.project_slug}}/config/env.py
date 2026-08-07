"""Typed environment access; application code must not read os.environ."""

from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Final, cast, overload

from django.core.exceptions import ImproperlyConfigured


_TRUE_VALUES: Final = frozenset({"1", "true", "t", "yes", "y", "on"})
_FALSE_VALUES: Final = frozenset({"0", "false", "f", "no", "n", "off"})


class Environment:
    """Parse explicitly declared runtime configuration values."""

    @staticmethod
    def _raw(name: str, default: object | None = None) -> object:
        value = os.environ.get(name)
        if value is not None:
            return value
        if default is not None:
            return default
        raise ImproperlyConfigured(f"Set the {name} environment variable.")

    @overload
    def string(self, name: str) -> str: ...

    @overload
    def string(self, name: str, default: str) -> str: ...

    def string(self, name: str, default: str | None = None) -> str:
        return str(self._raw(name, default))

    @overload
    def integer(self, name: str) -> int: ...

    @overload
    def integer(self, name: str, default: int) -> int: ...

    def integer(self, name: str, default: int | None = None) -> int:
        value = self._raw(name, default)
        try:
            return int(str(value).strip())
        except ValueError as exc:
            raise ImproperlyConfigured(f"{name} must be an integer.") from exc

    @overload
    def boolean(self, name: str) -> bool: ...

    @overload
    def boolean(self, name: str, default: bool) -> bool: ...

    def boolean(self, name: str, default: bool | None = None) -> bool:
        value = self._raw(name, default)
        if isinstance(value, bool):
            return value
        normalized = str(value).strip().lower()
        if normalized in _TRUE_VALUES:
            return True
        if normalized in _FALSE_VALUES:
            return False
        raise ImproperlyConfigured(f"{name} must be a boolean value.")

    def list(self, name: str, default: tuple[str, ...] = ()) -> list[str]:
        value = self._raw(name, default)
        if isinstance(value, str):
            return [
                item for item in (part.strip() for part in value.split(",")) if item
            ]
        return [
            str(item).strip()
            for item in cast(Iterable[object], value)
            if str(item).strip()
        ]


env = Environment()
