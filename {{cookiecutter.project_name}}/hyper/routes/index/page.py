from hyper.layouts.base import BaseLayout


class PageView(BaseLayout):
    route_name = "home"

    def __init__(self) -> None:
        super().__init__(title="Home")
        self.name = "Hello"
