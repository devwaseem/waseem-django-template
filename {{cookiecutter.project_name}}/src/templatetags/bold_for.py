from django import template
from django.utils.html import escape

from src.helpers.string import mark_as_strong_for

register = template.Library()


@register.filter(is_safe=True)
def bold_for(value: str, arg: str) -> str:
    """
    Make a part of text bold.

    Use `{% raw %}{{ "text_part_example"|bold_for:"example" }}{% endraw %}`
    """
    return mark_as_strong_for(escape(value), escape(arg))
