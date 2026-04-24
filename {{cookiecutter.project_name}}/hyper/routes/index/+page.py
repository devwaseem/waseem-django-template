from hyper.layouts.dashboard.layout import DashboardLayout


class PageView(DashboardLayout):
    route_name = "home"

    def __init__(self) -> None:
        super().__init__(title="Home")
        self.name = "Hello"
