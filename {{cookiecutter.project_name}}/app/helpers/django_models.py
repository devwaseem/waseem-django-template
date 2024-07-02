from typing import Type, TypeVar

from django.db.models import Model

T = TypeVar("T", bound=Model)


def get_object_or_none(model_class: Type[T], **kwargs: object) -> T | None:
    try:
        return model_class.objects.get(**kwargs)  # type: ignore
    except model_class.DoesNotExist:  # type: ignore
        return None
