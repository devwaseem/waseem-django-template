from hyper.layouts.base import BaseLayout


class PageView(BaseLayout):
    def __init__(self) -> None:
        super().__init__(title="Home")
        self.name = "Hello"
