from typing import Any

from allauth.account.views import SignupView
from django.http import HttpRequest, HttpResponse

from hyper.layouts.base import BaseLayout

from {{ cookiecutter.project_slug }}.platform.ratelimits import (
    enforce_public_auth_rate_limits,
)


class PageView(SignupView, BaseLayout):
    route_name = "account_signup"

    def __init__(self) -> None:
        super().__init__(title="Create Account")

    def dispatch(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        if request.method == "POST":
            enforce_public_auth_rate_limits(
                request,
                action="registration",
                email=request.POST.get("email", ""),
            )
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(
        self, context: dict[str, Any], **_response_kwargs: Any
    ) -> HttpResponse:
        html = self.render(
            request=self.request,
            context_updates=context,
        )
        return HttpResponse(html)
