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
def is_last_level(root_tag):
    return root_tag.children and all(is_leaf(child) for child in root_tag.children)


@register.filter
def is_leaf(root_tag):
    return not root_tag.children


@register.simple_tag
def create_timeline_labels(course):
    start_date, end_date = get_start_end_date(course.start_date, course.end_date)
    if not start_date or not end_date:
        return ''
    return mark_safe(f'"{start_date}", "{end_date}"')


@register.simple_tag
def create_timeline_datasets(course, tags, exercise_count_by_tag_slug_and_date):
    tag_names_by_slug = {tag.slug: tag.safe_name() for tag in tags}
    dataset_dicts = {}
    one_day = timezone.timedelta(days=1)
    start_date, end_date = get_start_end_date(course.start_date, course.end_date)

    for tag_slug, counts_by_date in exercise_count_by_tag_slug_and_date.items():
        if tag_slug not in tag_names_by_slug:
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
        f'{{label: "{tag_names_by_slug[tag_slug]}", data: [{",".join(counts_by_date)}]}}'
        for tag_slug, counts_by_date in dataset_dicts.items()
    ]

    return mark_safe(','.join(datasets))


@register.simple_tag
def create_progress_labels(root_tag, tag_stats):
    data = []
    for child in root_tag.children:
        stats = tag_stats[child.group]
        data.append(f'"  {child.name}: ({int(stats.points)}/{stats.total_exercises})"')
    return mark_safe(','.join(data))


@register.simple_tag
def create_progress_data(root_tag, tag_stats):
    data = []
    for child in root_tag.children:
        sub_tag_stats = tag_stats[child.group]
        data.append(str(sub_tag_stats.percent))
    return mark_safe(','.join(data))


@register.simple_tag
def create_background_progress_data(root_tag):
    return mark_safe(','.join('100' for _ in root_tag.children))


@register.simple_tag
def create_progress_colors(root_tag):
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
    return mark_safe(','.join(f'"{colors[i % len(colors)]}"' for i in range(len(root_tag.children))))


def get_start_end_date(start_date, end_date):
    if not start_date or not end_date:
        return start_date, end_date
    return start_date, min(end_date, timezone.now().date())
