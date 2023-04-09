from django.urls import URLPattern, URLResolver, path

from server.apps.main.views.home import HomeView

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="home")
]
