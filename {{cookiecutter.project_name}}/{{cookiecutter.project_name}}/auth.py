from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.request import Request

from .models.api_key import APIKey
from .models.user import User


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(
        self,
        request: Request,
    ) -> tuple[User | AnonymousUser, str | None]:
        api_key = request.META.get("HTTP_AUTHORIZATION")
        if not api_key:
            raise NotAuthenticated

        does_api_exists = APIKey.objects.filter(key=api_key.strip()).exists()
        if not does_api_exists:
            raise AuthenticationFailed

        return (AnonymousUser(), None)
