from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django import template
from django.forms.boundfield import BoundField
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


def _merge_classes(*values: object) -> str:
    parts: list[str] = []
    for value in values:
        if not value:
            continue
        parts.extend(str(value).split())

    return " ".join(dict.fromkeys(parts))


@register.simple_tag
def render_form_field(
    field: BoundField,
    attrs: Mapping[str, Any] | None = None,
    error_class: str = "",
    **kwargs: Any,
) -> SafeString:
    """Render a bound field with merged attributes and error classes."""

    final_attrs: dict[str, Any] = dict(attrs or {})

    for key, value in kwargs.items():
        if value in (None, "", False):
            continue

        attr_name = key.replace("__", "-").replace("_", "-")
        if attr_name == "class":
            final_attrs["class"] = _merge_classes(
                final_attrs.get("class"),
                value,
            )
            continue

        if value is True:
            final_attrs[attr_name] = attr_name
            continue

        final_attrs[attr_name] = value

    if field.errors and error_class:
        final_attrs["class"] = _merge_classes(
            final_attrs.get("class"),
            error_class,
        )

    return mark_safe(field.as_widget(attrs=final_attrs))
