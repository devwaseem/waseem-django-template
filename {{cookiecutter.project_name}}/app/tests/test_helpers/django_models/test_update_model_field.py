import faker
import pytest
from mixer.backend.django import mixer

from optik_invoice.helpers import django_models
from optik_invoice.models.account.user import User

fake = faker.Faker()


@pytest.mark.django_db
def test_throws_type_error_if_field_does_not_exist() -> None:
    expected_name = fake.name()
    user: User = mixer.blend(User, name="SOMETHING")  # type: ignore

    with pytest.raises(
        TypeError, match=f"__non_existent_field__ not found in {type(user)}"
    ):
        django_models.update_model_field(
            instance=user,
            attr="__non_existent_field__",
            value=expected_name,
        )


@pytest.mark.django_db
def test_updates_field_correctly_if_field_exists() -> None:
    expected_name = fake.name()
    user: User = mixer.blend(User, name="SOMETHING")  # type: ignore

    django_models.update_model_field(
        instance=user,
        attr="name",
        value=expected_name,
    )

    assert user.name == expected_name


@pytest.mark.django_db
def test_updates_field_correctly_with_cast_if_field_exists() -> None:
    user: User = mixer.blend(User, name="SOMETHING")  # type: ignore

    django_models.update_model_field(
        instance=user,
        attr="name",
        value=12345,
        cast=str,
    )

    assert user.name == "12345"
