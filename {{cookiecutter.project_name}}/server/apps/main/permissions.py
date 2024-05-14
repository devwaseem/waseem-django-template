from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import AccessMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from server.apps.main.models.api_key import APIKey

if TYPE_CHECKING:
    from rest_framework.views import APIView


class IsAPIKeyAuthenticated(BasePermission):
    def has_permission(self, request: Request, view: "APIView") -> bool:
        api_key = request.META.get("Authorization", "")

        return all(
            [
                super().has_permission(request, view),
                APIKey.objects.filter(key=api_key).exists(),
            ]
        )

    def has_object_permission(  # type: ignore
        self,
        request: Request,
        view: "APIView",
        _obj: Any,  # noqa: ANN401
    ) -> bool:
        return self.has_permission(request=request, view=view)


class SuperUserLoginRequiredMixin(AccessMixin):
    def dispatch(self, request: HttpRequest, *args: str, **kwargs: str) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)  # type: ignore

        return self.handle_no_permission()
