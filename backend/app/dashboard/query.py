from django.db.models.aggregates import Count
from core.models import Exercise, ExerciseTag, TelemetryData


def count_total_exercises_by_tag(course, tag_tree):
    tag_groups = _get_tag_groups(tag_tree)
    # ExerciseTag.objects.filter(course=course).aggregate(Count('exercise', filter='exercise__tags'), distinct=True))
    counts = {}
    tags_by_name = _get_tags_by_name(course, tag_tree)
    _count_total_exercises_by_tag_rec(counts, tag_tree, tags_by_name)
    return counts


def sum_points_by_tag(course, user, tag_tree):
    points = {}
    tags_by_name = _get_tags_by_name(course, tag_tree)
    # TODO CHECK FOR LAST SUBMISSION
    user_submissions = TelemetryData.objects.filter(author=user, exercise__course=course, exercise__tags__in=tags_by_name.values()).prefetch_related('exercise')
    _sum_points_by_tag_rec(points, tag_tree, tags_by_name, user_submissions)
    return points


def list_tags_from_tree(tag_tree):
    tags = set()
    tree_queue = [tag_tree]
    while tree_queue:
        tree = tree_queue.pop(0)
        for tag, subtree in tree.items():
            if isinstance(subtree, dict):
                tree_queue.append(subtree)
            tags.add(tag)
    return list(tags)


def _count_total_exercises_by_tag_rec(counts, tag_tree, tags_by_name, cur_group='', exercise_qs=None):
    total = 0
    for tag_name, subtree in tag_tree.items():
        new_group = f'{cur_group}/{tag_name}' if cur_group else tag_name
        tag = tags_by_name.get(tag_name)

        if not tag:
            new_exercises = Exercise.objects.none()
        else:
            if exercise_qs is None:
                new_exercises = tag.exercise_set.all()
            else:
                new_exercises = exercise_qs.intersection(tag.exercise_set.all())

        if isinstance(subtree, dict):
            counts[new_group] = _count_total_exercises_by_tag_rec(counts, subtree, tags_by_name, new_group, new_exercises)
        else:
            counts[new_group] = new_exercises.count()

        total += counts[new_group]

    return total


def _sum_points_by_tag_rec(points, tag_tree, tags_by_name, user_submissions):
    return


def _get_tag_groups(tag_tree):
    groups = []
    _get_tag_groups_rec(tag_tree, groups)
    return groups


def _get_tag_groups_rec(tag_tree, groups, cur_group = None):
    if cur_group is None:
        cur_group = []
    for tag_name, subtree in tag_tree.items():
        new_group = cur_group[:] + [tag_name]
        groups.append(new_group)
        if isinstance(subtree, dict):
            _get_tag_groups_rec(subtree, groups, new_group)


def _get_tags_by_name(course, tag_tree):
    tags = list_tags_from_tree(tag_tree)
    all_tags = ExerciseTag.objects.filter(course=course, name__in=tags).prefetch_related('exercise_set')
    return {t.name: t for t in all_tags}
