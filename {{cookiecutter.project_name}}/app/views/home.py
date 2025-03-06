from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View
from frontend.pages.root.home import HomePage, HomePageProps


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HomePage(props=HomePageProps()).as_response()
