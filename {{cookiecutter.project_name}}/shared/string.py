def unique_split(string: str, *, delimiter: str) -> list:
    return list(
        set(
            filter(
                lambda value: value != "",
                map(str.strip, string.rstrip(delimiter).split(delimiter)),
            ),
        ),
    )
