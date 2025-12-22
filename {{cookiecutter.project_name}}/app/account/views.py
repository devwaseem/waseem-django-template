from __future__ import annotations

from typing import cast

from django.conf import settings
from django.contrib.auth import aauthenticate, alogin, alogout
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from frontend.pages.auth.login import LoginPage

from app.account.forms import LoginForm

LOGIN_URL = cast(str, settings.LOGIN_REDIRECT_URL)


class LoginView(View):
    async def get(self, request: HttpRequest) -> HttpResponse:
        user = await request.auser()
        if user.is_authenticated:
            return self._redirect_after_login(
                request=request, default_redirect=LOGIN_URL
            )

        next_url = request.GET.get("next", "")
        return LoginPage(
            form=LoginForm(),
            next_url=next_url,
        ).as_response(request=request)

    async def post(self, request: HttpRequest) -> HttpResponse:
        user = await request.auser()
        if user.is_authenticated:
            return self._redirect_after_login(
                request=request,
                default_redirect=LOGIN_URL,
            )

        form = LoginForm(request.POST)
        if not form.is_valid():
            return LoginPage(
                form=form,
                next_url=request.POST.get("next", ""),
            ).as_response(request=request)

        authenticated_user = await aauthenticate(
            request=request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )

        if authenticated_user is None or not authenticated_user.is_active:
            form.add_error(
                field=None,
                error="Invalid email or password.",
            )
            return LoginPage(
                form=form,
                next_url=request.POST.get("next", ""),
            ).as_response(request=request)

        await alogin(request, authenticated_user)

        return self._redirect_after_login(
            request=request,
            default_redirect=LOGIN_URL,
        )

    def _redirect_after_login(
        self, request: HttpRequest, default_redirect: str
    ) -> HttpResponseRedirect:
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return HttpResponseRedirect(next_url)

        return HttpResponseRedirect(default_redirect)


class LogoutView(View):
    async def post(self, request: HttpRequest) -> HttpResponse:
        await alogout(request)
        return HttpResponseRedirect(reverse("account:login"))
