from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from core.models import Course, Exercise, ExerciseTag, Instructor, Student, TelemetryData
from dashboard.query import (count_total_exercises_by_tag_group, get_all_tags,
                             get_exercise_ids_and_tags,
                             get_exercise_ids_by_tag_group,
                             get_exercise_ids_by_tag_name, list_tags_from_tree,
                             sum_points_by_tag_group)
from dashboard.views import student_dashboard


class DashboardTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.course = Course.objects.create(name='Awesome Course')
        self.student = Student.objects.create_user(username='gandalf', email='thegray@middleearth.nz', password='you-shall-not-pass')
        self.other_student = Student.objects.create_user(username='saruman', email='thewhite@middleearth.nz', password='the-hour-is-later-than-you-think')
        self.instructor = Instructor.objects.create_user(username='tolkien', email='jrrt@ox.ac.uk', password='not-all-those-who-wander-are-lost')

    def test_student_cant_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/{self.course.name}/student/{self.student.id}')
        request.user = self.other_student

        self.assertRaises(PermissionDenied, student_dashboard, request, self.course.name, self.student.id)

    def test_student_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/{self.course.name}/student/{self.student.id}')
        request.user = self.student

        assert student_dashboard(request, self.course.name, self.student.id) is not None

    def test_instructor_can_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/{self.course.name}/fragments/student/{self.student.id}')
        request.user = self.instructor

        assert student_dashboard(request, self.course.name, self.student.id) is not None

    def test_instructor_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/{self.course.name}/fragments/student/{self.instructor.id}')
        request.user = self.instructor

        assert student_dashboard(request, self.course.name, self.instructor.id) is not None


class QueryTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create_user('gandalf', 'thegray@middleearth.nz', 'you-shall-not-pass')
        self.other_student = Student.objects.create_user(username='saruman', email='thewhite@middleearth.nz', password='the-hour-is-later-than-you-think')
        self.course = Course.objects.create(name='Awesome Course')
        self.other_course = Course.objects.create(name='Not So Awesome Course')
        self.tag_tree = {
            'python': {
                'name': 'Python',
                'children': {
                    'if': 'If',
                    'while': 'While',
                }
            },
            'design': 'Design',
        }
        self.tag_names = ['python', 'if', 'while', 'design']

    def test_list_tags_from_tree(self):
        expected = sorted(
            ['python', 'if', 'while', 'design']
        )
        assert expected == sorted(list_tags_from_tree(self.tag_tree))

    def test_get_all_tags(self):
        tags = sorted(self._create_tags(self.course), key=lambda t: t.name)
        self._create_tags(self.other_course)

        with self.assertNumQueries(1):
            self.assertQuerysetEqual(get_all_tags(self.course, self.tag_tree).order_by('name'), tags)

    def test_get_exercise_ids_and_tags(self):
        tags = self._create_tags(self.course)
        self._create_tags(self.other_course)

        tag_groups = ['python/if', 'python/while', 'design']
        exercises = self._create_exercises_for_tag_groups(tag_groups, 2, self.course)
        self._create_exercises_for_tag_groups(tag_groups, 2, self.other_course, len(exercises))

        tag_ids = {t.name: t.id for t in tags}
        expected = sorted([
            (1, tag_ids['python']), (1, tag_ids['if']),
            (2, tag_ids['python']), (2, tag_ids['if']),
            (3, tag_ids['python']), (3, tag_ids['while']),
            (4, tag_ids['python']), (4, tag_ids['while']),
            (5, tag_ids['design']),
            (6, tag_ids['design']),
        ])
        with self.assertNumQueries(1):
            exercise_ids_and_tags = sorted(get_exercise_ids_and_tags(self.course))

        assert expected == exercise_ids_and_tags, f'Expected: {expected}. Got: {exercise_ids_and_tags}'

    def test_get_exercise_ids_by_tag_name(self):
        tags = self._create_tags(self.course)
        tag_ids = {t.name: t.id for t in tags}
        exercise_ids_and_tags = [
            (1, tag_ids['python']), (1, tag_ids['if']),
            (2, tag_ids['python']), (2, tag_ids['while']),
            (3, tag_ids['while']),
        ]

        expected = {
            'python': {1, 2},
            'if': {1},
            'while': {2, 3},
        }

        with self.assertNumQueries(0):
            exercise_ids_by_tag_name = get_exercise_ids_by_tag_name(exercise_ids_and_tags, tags)

        assert expected == exercise_ids_by_tag_name, f'Expected: {expected}. Got: {exercise_ids_by_tag_name}'

    def test_get_exercise_ids_by_tag_group(self):
        exercise_ids_by_tag_name = {
            'python': {1, 2, 3, 4, 5},
            'if': {1, 2},
            'while': {3, 4, 6},
        }

        expected = {
            'python': {1, 2, 3, 4, 5},
            'python/if': {1, 2},
            'python/while': {3, 4},
            'design': set(),
        }
        with self.assertNumQueries(0):
            exercise_ids_by_tag_group = get_exercise_ids_by_tag_group(self.tag_tree, exercise_ids_by_tag_name)

        assert expected == exercise_ids_by_tag_group, f'Expected: {expected}. Got: {exercise_ids_by_tag_group}'


    def test_count_total_exercises_for_tag_tree(self):
        exercise_ids_by_tag_group = {
            'python': {1, 2, 3, 4, 5},
            'python/if': {1, 2},
            'python/while': {3, 4},
            'design': {},
        }

        expected = {
            'python': 5,
            'python/if': 2,
            'python/while': 2,
            'design': 0,
        }

        with self.assertNumQueries(0):
            assert expected == count_total_exercises_by_tag_group(exercise_ids_by_tag_group)

    def test_sum_points_for_tag_tree(self):
        self._create_tags(self.course)
        self._create_tags(self.other_course)
        ExerciseTag.objects.create(name='choice', course=self.course)
        ExerciseTag.objects.create(name='choice', course=self.other_course)

        tag_groups = ['python/if', 'python/while', 'python/while/choice', 'python/choice', 'design', 'design/choice']
        exercises = self._create_exercises_for_tag_groups(tag_groups, 1, self.course)
        exercises += self._create_exercises_for_tag_groups(tag_groups, 1, self.other_course, len(exercises))

        final_pts = 0.5
        self._create_submissions_for(self.student, exercises, [0.3, 0.7, final_pts], ['python/if'])
        self._create_submissions_for(self.other_student, exercises, [0.3, 0.7, final_pts], ['python/if'])

        exercise_ids_by_tag_group = {
            'python': {1, 2, 3, 4, 5},
            'python/if': {1},
            'python/while': {2, 3},
            'python/while/choice': {3},
            'python/choice': {4},
            'design': {5},
            'python/choice': {6},
        }

        # We consider the last submission, so it's 0.5 points per exercise, skipping 'python/if'
        expected = {
            'python': 4 * final_pts,
            'python/if': 0 * final_pts,
            'python/while': 2 * final_pts,
            'python/while/choice': 1 * final_pts,
            'python/choice': 1 * final_pts,
            'design': 1 * final_pts,
            'python/choice': 1 * final_pts,
        }

        with self.assertNumQueries(1):
            points_by_tag_group = sum_points_by_tag_group(self.student, self.course, exercise_ids_by_tag_group)

        assert expected == points_by_tag_group, f'Expected: {expected}. Got: {points_by_tag_group}.'

    def _create_tags(self, course):
        tags = [
            ExerciseTag(name=tag_name, course=course)
            for tag_name in self.tag_names
        ]
        return ExerciseTag.objects.bulk_create(tags)

    def _create_exercises_for_tag_groups(self, tag_groups, total_per_group, course, start_from_id=0):
        exercises = []
        for i, tag_group in enumerate(tag_groups):
            for j in range(total_per_group):
                exercise = Exercise.objects.create(course=course, slug=f'Exercise {start_from_id + i * total_per_group + j}')
                tags = tag_group.split('/')
                for tag_name in tags:
                    tag = ExerciseTag.objects.get(course=course, name=tag_name)
                    exercise.tags.add(tag)
                exercise.save()
                exercises.append(exercise)
        return exercises

    def _create_submissions_for(self, author, exercises, points_per_exercise, skip_list):
        skip_list = [skip.split('/') for skip in skip_list]
        for points in points_per_exercise:
            for exercise in exercises:
                tags = exercise.tags.all()

                should_skip = False
                for skip in skip_list:
                    if all(t.name in skip for t in tags):
                        should_skip = True

                if not should_skip:
                    TelemetryData.objects.create(author=author, exercise=exercise, points=points, log={})
