from dataclasses import asdict, dataclass
from django.http import HttpRequest


@dataclass(slots=True, frozen=True)
class EmailCommonContext:
    logo_light_url: str | None
    logo_dark_url: str | None

    def as_dict(self):
        return asdict(self)


def get_common_email_context(request: HttpRequest) -> EmailCommonContext:
    raise NotImplementedError()
