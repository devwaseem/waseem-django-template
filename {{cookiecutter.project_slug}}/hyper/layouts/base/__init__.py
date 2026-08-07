from typing import Any

from django.http import HttpRequest
from hyperdjango.page import HyperView


class BaseLayout(HyperView):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        context = super().get_context(request)
        context["title"] = self.title
        return context
