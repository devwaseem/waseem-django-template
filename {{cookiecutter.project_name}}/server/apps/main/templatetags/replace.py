from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    """
    Replacing filter.

    Use `{% raw %}{{ "aaa"|replace:"a|b" }}{% endraw %}`
    """
    if len(arg.split("|")) != 2:
        return value

    what, to = arg.split("|")
    return value.replace(what, to)
