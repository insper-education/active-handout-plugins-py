from django import template

register = template.Library()

@register.filter
def get_value(dict_like, key):
    if not hasattr(dict_like, 'get'):
        return None
    return dict_like.get(key)


@register.filter
def add_to_group(tag_group, new_tag):
    if not tag_group:
        return new_tag
    return f'{tag_group}/{new_tag}'
