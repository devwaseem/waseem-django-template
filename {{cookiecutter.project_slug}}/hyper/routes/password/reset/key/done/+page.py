from typing import Any

from allauth.account.views import PasswordResetFromKeyDoneView
from django.http import HttpResponse, HttpResponseBase

from hyper.layouts.base import BaseLayout


class PageView(BaseLayout, PasswordResetFromKeyDoneView):
    route_name = "account_reset_password_from_key_done"

    def __init__(self) -> None:
        super().__init__(title="Password Updated")

    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponseBase:
        return PasswordResetFromKeyDoneView.dispatch(self, request, *args, **kwargs)

    def render_to_response(
        self, context: dict[str, Any], **_response_kwargs: Any
    ) -> HttpResponse:
        html = self.render(
            request=self.request,
            context_updates=context,
        )
        return HttpResponse(html)
