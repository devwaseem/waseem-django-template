import pytest
from mixer.backend.django import mixer

from app.helpers import django_models
from app.models.account.user import User


@pytest.mark.django_db
def test_returns_none_if_object_does_not_exist() -> None:
    User.objects.filter(
        id=123
    ).delete()  # making sure user with id 123 does not exist

    sut = django_models.get_object_or_none(User, id=123)

    assert sut is None


@pytest.mark.django_db
def test_returns_object_if_object_exist() -> None:
    mixer.blend(User, id=123)  # create user with id 123

    sut = django_models.get_object_or_none(User, id=123)

    assert sut is not None
