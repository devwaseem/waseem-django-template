from typing import Any

from allauth.account.views import PasswordResetFromKeyView
from django.http import HttpResponse

from hyper.layouts.base import BaseLayout


class PageView(BaseLayout, PasswordResetFromKeyView):
    def __init__(self) -> None:
        super().__init__(title="Set New Password")

    def dispatch(
        self, request: Any, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        return PasswordResetFromKeyView.dispatch(
            self, request, *args, **kwargs
        )

    def render_to_response(
        self, context: dict[str, Any], **_response_kwargs: Any
    ) -> HttpResponse:
        html = self.render(
            request=self.request,
            context_updates=context,
        )
        return HttpResponse(html)
