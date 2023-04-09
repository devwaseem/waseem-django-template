from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    template_name = "main/templates/home.html"

    def get(self, request: HttpRequest):
        return render(
            request=request,
            template_name=self.template_name,
            context={},
        )
