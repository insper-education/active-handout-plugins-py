from django.utils import timezone

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
def create_timeline_labels(course):
    start_date, end_date = get_start_end_date(course.start_date, course.end_date)
    if not start_date or not end_date:
        return ''
    return mark_safe(f'"{start_date}", "{end_date}"')


@register.simple_tag
def create_timeline_datasets(course, tags, exercise_count_by_tag_slug_and_date):
    all_tag_slugs = set(tag.slug for tag in tags)
    dataset_dicts = {}
    one_day = timezone.timedelta(days=1)
    start_date, end_date = get_start_end_date(course.start_date, course.end_date)

    for tag_slug, counts_by_date in exercise_count_by_tag_slug_and_date.items():
        if tag_slug not in all_tag_slugs:
            continue

        updated_counts = {}
        for date, total in counts_by_date.items():
            updated_counts[date] = total
            yesterday = date - one_day
            tomorrow = date + one_day
            if yesterday not in updated_counts and yesterday > start_date:
                updated_counts[yesterday] = 0
            if tomorrow not in counts_by_date and tomorrow < end_date:
                updated_counts[tomorrow] = 0

        if start_date not in updated_counts:
            updated_counts[start_date] = 0
        if end_date not in updated_counts:
            updated_counts[end_date] = 0

        dataset_dicts[tag_slug] = []
        for date in sorted(updated_counts):
            dataset_dicts[tag_slug].append(f'{{x: "{date}", y: {updated_counts[date]}}}')

    datasets = [
        f'{{label: "{tag_slug}", data: [{",".join(counts_by_date)}]}}'
        for tag_slug, counts_by_date in dataset_dicts.items()
    ]

    return mark_safe(','.join(datasets))


@register.simple_tag
def create_progress_labels(tag_tree, tag_stats, group):
    data = []
    for tag, tag_slug in tag_tree.items():
        tag_group = add_to_group(group, tag)
        stats = tag_stats[tag_group]
        data.append(f'"  {tag_slug}: ({int(stats.points)}/{stats.total_exercises})"')
    return mark_safe(','.join(data))


@register.simple_tag
def create_progress_data(tag_tree, tag_stats, group):
    data = []
    for sub_tag in tag_tree:
        sub_tag_group = add_to_group(group, sub_tag)
        sub_tag_stats = tag_stats[sub_tag_group]
        data.append(str(sub_tag_stats.percent))
    return mark_safe(','.join(data))


@register.simple_tag
def create_background_progress_data(tag_tree):
    return mark_safe(','.join('100' for _ in tag_tree))


@register.simple_tag
def create_progress_colors(tag_tree):
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


def get_start_end_date(start_date, end_date):
    if not start_date or not end_date:
        return start_date, end_date
    return start_date, min(end_date, timezone.now().date())
