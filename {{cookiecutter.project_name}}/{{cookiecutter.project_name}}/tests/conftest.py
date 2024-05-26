import tempfile
from typing import Any, Generator

import pytest


@pytest.fixture(autouse=True)
def _set_tmp_media_storage(settings: Any) -> Generator[None, Any, None]:  # noqa
    tempdir = tempfile.TemporaryDirectory(prefix="test")
    settings.STORAGES["default"]["OPTIONS"]["location"] = tempdir.name
    yield
    tempdir.cleanup()
