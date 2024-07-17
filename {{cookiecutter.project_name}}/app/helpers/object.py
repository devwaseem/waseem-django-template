from typing import Any, TypeVar


def has_any_field_valid(obj: Any, *, fields: list[str]) -> bool:  # type: ignore
    for field in fields:
        value = getattr(obj, field)
        if value:
            return True
    return False


T = TypeVar("T")


def object_or_none(  # type: ignore
    *,
    condition: bool | Any | None,
    return_value: T | None,
) -> T | None:  # type: ignore
    if isinstance(condition, bool):
        if condition:
            return return_value
        return None
    if condition:
        return return_value
    return None


def value_or_none(  # type: ignore
    return_value: T | None,
) -> T | None:  # type: ignore
    if return_value is not None:
        return return_value
    return None
