from django import template
from django.utils.safestring import mark_safe

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


@register.filter
def is_last_level(tag_group):
    if is_leaf(tag_group):
        return False
    return all(is_leaf(child) for child in tag_group.values())


@register.filter
def is_leaf(sub_tree):
    return not isinstance(sub_tree, dict)


@register.simple_tag
def create_labels(tag_tree, tag_stats, group):
    data = []
    for tag, tag_name in tag_tree.items():
        tag_group = add_to_group(group, tag)
        stats = tag_stats[tag_group]
        data.append(f'"  {tag_name}: ({int(stats.points)}/{stats.total_exercises})"')
    return mark_safe(','.join(data))


@register.simple_tag
def create_data(tag_tree, tag_stats, group):
    data = []
    for sub_tag in tag_tree:
        sub_tag_group = add_to_group(group, sub_tag)
        sub_tag_stats = tag_stats[sub_tag_group]
        data.append(str(sub_tag_stats.percent))
    return mark_safe(','.join(data))


@register.simple_tag
def create_background_data(tag_tree):
    return mark_safe(','.join('100' for _ in tag_tree))


@register.simple_tag
def create_colors(tag_tree):
    colors = [
      '#4dc9f6',
      '#f67019',
      '#f53794',
      '#537bc4',
      '#acc236',
      '#166a8f',
      '#00a950',
      '#58595b',
      '#8549ba'
    ]
    return mark_safe(','.join(f'"{colors[i % len(colors)]}"' for i in range(len(tag_tree))))
