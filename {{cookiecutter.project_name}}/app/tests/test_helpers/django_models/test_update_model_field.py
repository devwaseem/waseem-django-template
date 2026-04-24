from typing import cast

import faker
import pytest
from mixer.backend.django import mixer

from app.account.models import User
from app.helpers import django_models

fake = faker.Faker()


@pytest.mark.django_db
def test_throws_type_error_if_field_does_not_exist() -> None:
    expected_first_name = fake.first_name()
    user = cast(User, mixer.blend(User, first_name="SOMETHING"))

    with pytest.raises(
        TypeError, match=f"__non_existent_field__ not found in {type(user)}"
    ):
        django_models.update_model_field(
            instance=user,
            attr="__non_existent_field__",
            value=expected_first_name,
        )


@pytest.mark.django_db
def test_updates_field_correctly_if_field_exists() -> None:
    expected_first_name = fake.first_name()
    user = cast(User, mixer.blend(User, first_name="SOMETHING"))

    django_models.update_model_field(
        instance=user,
        attr="first_name",
        value=expected_first_name,
    )

    assert user.first_name == expected_first_name


@pytest.mark.django_db
def test_updates_field_correctly_with_cast_if_field_exists() -> None:
    user = cast(User, mixer.blend(User, first_name="SOMETHING"))

    django_models.update_model_field(
        instance=user,
        attr="first_name",
        value=12345,
        cast=str,
    )

    assert user.first_name == "12345"
