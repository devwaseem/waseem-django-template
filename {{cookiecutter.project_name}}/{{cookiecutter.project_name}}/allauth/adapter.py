import typing
from typing import Any

from django.conf import settings
from django.http import HttpRequest

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin

from {{cookiecutter.project_name}}.context_processors import get_site_data
from {{cookiecutter.project_name}}.models.user import User


class AllAuthAccountAdapter(DefaultAccountAdapter):  # type: ignore
    request: HttpRequest

    def is_open_for_signup(self, _request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def send_mail(  # type: ignore
        self,
        template_prefix: str,
        email: str,
        context: dict[str, Any],
    ) -> None:
        context.update(get_site_data(request=self.request))
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def format_email_subject(self, subject: str) -> str:
        site_data = get_site_data(request=self.request)
        prefix = site_data["site_name"]
        if prefix is None:
            return subject
        return f"{prefix}: {subject}"


class SocialAccountAdapter(DefaultSocialAccountAdapter):  # type: ignore
    def is_open_for_signup(
        self,
        _request: HttpRequest,
        _sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(  # type: ignore
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user: User = super().populate_user(request, sociallogin, data)
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        return user
