from typing import TypeVar

T = TypeVar("T")
V = TypeVar("V")


def remove_none_from_dict(
    initial: dict[T, V | None],
    *,
    nested: bool = True,
    remove_empty_strings: bool = False,
) -> dict[T, V]:
    new_dict = {}
    for key, value in initial.items():
        if value is None:
            continue

        if isinstance(value, dict):
            if not nested:
                new_dict[key] = value  # type: ignore
                continue
            new_dict[key] = remove_none_from_dict(
                initial=value,
                nested=nested,
                remove_empty_strings=remove_empty_strings,
            )
        elif isinstance(value, str):
            if remove_empty_strings and value == "":
                continue
            new_dict[key] = value  # type: ignore
        else:
            new_dict[key] = value  # type: ignore
    return new_dict  # type: ignore
