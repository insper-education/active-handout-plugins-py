from dataclasses import dataclass
from core.models import Exercise, ExerciseTag, TelemetryData


@dataclass
class TagGroupStats:
    tag_group: str
    total_exercises: int
    points: float = 0


def get_stats_by_tag_group(tag_tree, course, author):
    tags = get_all_tags(course, tag_tree)
    exercise_ids_and_tags = get_exercise_ids_and_tags(course)
    exercise_ids_by_tag_name = get_exercise_ids_by_tag_name(exercise_ids_and_tags, tags)
    exercise_ids_by_tag_group = get_exercise_ids_by_tag_group(tag_tree, exercise_ids_by_tag_name)

    total_exercises_by_tag_group = count_total_exercises_by_tag_group(exercise_ids_by_tag_group)
    points_by_tag_group = sum_points_by_tag_group(author, course, exercise_ids_by_tag_group)

    return {
        tag_group: TagGroupStats(
            tag_group,
            total_exercises_by_tag_group[tag_group],
            points_by_tag_group[tag_group]
        ) for tag_group in total_exercises_by_tag_group
    }


def count_total_exercises_by_tag_group(exercise_ids_by_tag_group):
    counts = {tag_group: len(ids) for tag_group, ids in exercise_ids_by_tag_group.items()}
    return counts


def sum_points_by_tag_group(user, course, exercise_ids_by_tag_group):
    points_by_exercise_id = dict(TelemetryData.objects.filter(author=user, exercise__course=course, last=True).values_list('exercise_id', 'points'))
    points = {
        tag_group: sum(points_by_exercise_id.get(eid, 0) for eid in exercise_ids)
        for tag_group, exercise_ids in exercise_ids_by_tag_group.items()
    }
    return points


def list_tags_from_tree(tag_tree):
    tags = set()
    tree_queue = [{'children': tag_tree}]
    while tree_queue:
        tree = tree_queue.pop(0)
        children = tree['children']
        for tag, subtree in children.items():
            if isinstance(subtree, dict):
                tree_queue.append(subtree)
            tags.add(tag)
    return list(tags)


def get_all_tags(course, tag_tree):
    tags = list_tags_from_tree(tag_tree)
    return ExerciseTag.objects.filter(course=course, name__in=tags)


def get_exercise_ids_by_tag_name(exercise_ids_and_tags, tags):
    tags_by_id = {t.id: t for t in tags}
    exercise_ids_by_tag = {}
    for exercise_id, tag_id in exercise_ids_and_tags:
        tag = tags_by_id.get(tag_id)
        if tag is not None:
            exercise_ids_by_tag.setdefault(tag.name, set()).add(exercise_id)
    return exercise_ids_by_tag


def get_exercise_ids_by_tag_group(tag_tree, exercise_ids_by_tag_name):
    by_tag_group = {}
    _get_exercise_ids_by_tag_group_rec(by_tag_group, {'children': tag_tree}, exercise_ids_by_tag_name)
    return by_tag_group


def get_exercise_ids_and_tags(course):
    return Exercise.objects.filter(course=course).values_list('id', 'tags')


def _get_exercise_ids_by_tag_group_rec(by_tag_group, tag_tree, exercise_ids_by_tag_name, cur_group='', cur_set=None):
    for tag_name, subtree in tag_tree['children'].items():
        new_group = f'{cur_group}/{tag_name}' if cur_group else tag_name
        exercise_ids = exercise_ids_by_tag_name.get(tag_name, set())
        new_set = exercise_ids if cur_set is None else cur_set & exercise_ids
        by_tag_group[new_group] = new_set

        if isinstance(subtree, dict):
            _get_exercise_ids_by_tag_group_rec(by_tag_group, subtree, exercise_ids_by_tag_name, new_group, new_set)
