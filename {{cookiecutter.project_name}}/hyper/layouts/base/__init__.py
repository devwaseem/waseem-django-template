from hyperdjango.page import HyperView


class BaseLayout(HyperView):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
