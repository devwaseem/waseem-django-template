from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    template_name = "home.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name=self.template_name,
            context={},
        )
