from dataclasses import dataclass

from django.db.models import F

from core.models import Exercise, ExerciseTag, TelemetryData


@dataclass
class TagGroupStats:
    tag_group: str
    total_exercises: int
    points: float = 0

    @property
    def percent(self):
        if self.total_exercises == 0:
            return 0
        return 100 * self.points / self.total_exercises


class StudentStats:
    def __init__(self, student, course, tag_tree):
        self.student = student
        self.course = course
        self.tag_tree = tag_tree

        self.tags = get_all_tags(course, tag_tree)
        self.exercise_ids_and_tags = get_exercise_ids_and_tags(course)
        self.exercise_ids_by_tag_name = get_exercise_ids_by_tag_name(self.exercise_ids_and_tags, self.tags)
        self.exercise_ids_by_tag_group = get_exercise_ids_by_tag_group(tag_tree, self.exercise_ids_by_tag_name)
        self.points_by_exercise_id = get_points_by_exercise_id(student, course)

        self.total_exercises_by_tag_group = count_total_exercises_by_tag_group(self.exercise_ids_by_tag_group)
        self.points_by_tag_group = sum_points_by_tag_group(self.points_by_exercise_id, self.exercise_ids_by_tag_group)

        self.stats_by_tag_group = {
            tag_group: TagGroupStats(
                tag_group,
                self.total_exercises_by_tag_group[tag_group],
                self.points_by_tag_group[tag_group]
            ) for tag_group in self.total_exercises_by_tag_group
        }

        self.total_exercises = len(self.points_by_exercise_id)

        self.execise_ids_by_date = get_exercise_ids_by_date(student, course)
        self.exercises_by_id = get_exercises_by_id(course)
        self.exercise_count_by_tag_name_and_date = get_exercise_count_by_tag_name_and_date(self.execise_ids_by_date, self.exercises_by_id)


def count_total_exercises_by_tag_group(exercise_ids_by_tag_group):
    counts = {tag_group: len(ids) for tag_group, ids in exercise_ids_by_tag_group.items()}
    return counts


def get_points_by_exercise_id(user, course):
    return dict(TelemetryData.objects.filter(author=user, exercise__course=course, last=True).values_list('exercise_id', 'points'))


def sum_points_by_tag_group(points_by_exercise_id, exercise_ids_by_tag_group):
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


def get_exercise_ids_by_date(student, course):
    if not course.start_date or not course.end_date:
        return {}

    dates_and_ids = (
        TelemetryData.objects
            .filter(
                author=student,
                exercise__course=course,
                submission_date__gte=course.start_date,
                submission_date__lte=course.end_date,
            )
            .values('submission_date')
            .annotate(exercise_id=F('exercise_id'))
            .distinct()
            .values_list('submission_date', 'exercise_id')
    )
    ids_by_date = {}
    for date, exercise_id in dates_and_ids:
        ids_by_date.setdefault(date.date(), []).append(exercise_id)
    return ids_by_date


def get_exercise_count_by_tag_name_and_date(exercise_ids_by_date, exercises_by_id):
    counts = {}
    for date, exercise_ids in exercise_ids_by_date.items():
        for exercise_id in exercise_ids:
            exercise = exercises_by_id[exercise_id]
            for tag in exercise.tags.all():
                tag_name = tag.name
                tag_counts = counts.setdefault(tag_name, {})
                tag_counts[date] = tag_counts.get(date, 0) + 1
    return counts


def get_exercises_by_id(course):
    return {exercise.id: exercise for exercise in Exercise.objects.filter(course=course).prefetch_related('tags')}


def _get_exercise_ids_by_tag_group_rec(by_tag_group, tag_tree, exercise_ids_by_tag_name, cur_group='', cur_set=None):
    for tag_name, subtree in tag_tree['children'].items():
        new_group = f'{cur_group}/{tag_name}' if cur_group else tag_name
        exercise_ids = exercise_ids_by_tag_name.get(tag_name, set())
        new_set = exercise_ids if cur_set is None else cur_set & exercise_ids
        by_tag_group[new_group] = new_set

        if isinstance(subtree, dict):
            _get_exercise_ids_by_tag_group_rec(by_tag_group, subtree, exercise_ids_by_tag_name, new_group, new_set)
