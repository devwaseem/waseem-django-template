from typing import Any

from allauth.account.views import LoginView
from django.http import HttpResponse

from hyper.layouts.base import BaseLayout


class PageView(LoginView, BaseLayout):
    route_name = "account_login"

    def __init__(self) -> None:
        super().__init__(title="Login")

    def render_to_response(
        self, context: dict[str, Any], **_response_kwargs: Any
    ) -> HttpResponse:
        html = self.render(
            request=self.request,
            context_updates=context,
        )
        return HttpResponse(html)
