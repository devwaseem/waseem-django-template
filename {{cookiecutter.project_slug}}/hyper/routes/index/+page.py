from django.contrib.auth.mixins import LoginRequiredMixin

from hyper.layouts.dashboard.layout import DashboardLayout


class PageView(LoginRequiredMixin, DashboardLayout):
    route_name = "home"

    def __init__(self) -> None:
        super().__init__(title="Home")
