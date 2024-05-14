import uuid

from django import template

register = template.Library()


@register.filter
def uuid4(value: str) -> str:
    """
    generate random filter.

    Use `{% raw %}{{ "uuid4"|uuid4 }}{% endraw %}`
    """
    return value.replace("uuid4", str(uuid.uuid4()))
