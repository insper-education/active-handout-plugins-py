from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from core.models import ExerciseTag
from dashboard.query import (count_total_exercises_by_tag_group, get_all_tags,
                             get_exercise_ids_and_tags,
                             get_exercise_ids_by_tag_group,
                             get_exercise_ids_by_tag_name,
                             get_points_by_exercise_id, list_tags_from_tree,
                             sum_points_by_tag_group)
from dashboard.test_utils import (BuildACourse, BuildAnInstructor,
                                  BuildAStudent, BuildExercises, BuildTags,
                                  BuildTelemetryDatas)
from dashboard.views import student_dashboard


class DashboardTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.course = (
            BuildACourse()
                .called('Awesome Course')
                .build()
        )
        self.student = (
            BuildAStudent()
                .with_username('gandalf')
                .with_email('thegray@middleearth.nz')
                .with_password('you-shall-not-pass')
                .build()
        )
        self.other_student = (
            BuildAStudent()
                .with_username('saruman')
                .with_email('thewhite@middleearth.nz')
                .with_password('the-hour-is-later-than-you-think')
                .build()
        )
        self.instructor = (
            BuildAnInstructor()
                .with_username('tolkien')
                .with_email('jrrt@ox.ac.uk')
                .with_password('not-all-those-who-wander-are-lost')
                .build()
        )

    def test_student_cant_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/{self.course.name}/student/{self.student.id}')
        request.user = self.other_student

        self.assertRaises(PermissionDenied, student_dashboard, request, self.course.name, self.student.id)

    def test_student_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/{self.course.name}/student/{self.student.id}')
        request.user = self.student

        self.assertIsNotNone(student_dashboard(request, self.course.name, self.student.id))

    def test_instructor_can_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/{self.course.name}/fragments/student/{self.student.id}')
        request.user = self.instructor

        self.assertIsNotNone(student_dashboard(request, self.course.name, self.student.id))

    def test_instructor_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/{self.course.name}/fragments/student/{self.instructor.id}')
        request.user = self.instructor

        self.assertIsNotNone(student_dashboard(request, self.course.name, self.instructor.id))


class QueryTests(TestCase):
    def setUp(self):
        self.student = (
            BuildAStudent()
                .with_username('gandalf')
                .with_email('thegray@middleearth.nz')
                .with_password('you-shall-not-pass')
                .build()
        )
        self.other_student = (
            BuildAStudent()
                .with_username('saruman')
                .with_email('thewhite@middleearth.nz')
                .with_password('the-hour-is-later-than-you-think')
                .build()
        )
        self.course = BuildACourse().called('Awesome Course').build()
        self.other_course = BuildACourse().called('Not So Awesome Course').build()
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
        self.assertListEqual(expected, sorted(list_tags_from_tree(self.tag_tree)))

    def test_get_all_tags(self):
        BuildTags().for_course(self.other_course).with_names(*self.tag_names).build()
        course_tags = BuildTags().for_course(self.course).with_names(*self.tag_names).build()
        course_tags = sorted(course_tags, key=lambda t: t.name)

        with self.assertNumQueries(1):
            self.assertQuerysetEqual(
                get_all_tags(self.course, self.tag_tree).order_by('name'),
                course_tags
            )

    def test_get_exercise_ids_and_tags(self):
        BuildTags().for_course(self.other_course).with_names(*self.tag_names).build()
        BuildTags().for_course(self.course).with_names(*self.tag_names).build()

        tag_groups = ['python/if', 'python/while', 'design']

        (BuildExercises()
            .for_course(self.other_course)
            .for_tag_groups(tag_groups)
            .each_group_with(2)
            .build())
        exercises = (
            BuildExercises()
                .for_course(self.course)
                .for_tag_groups(tag_groups)
                .each_group_with(2)
                .build()
        )

        expected = sorted([
            (exercise.id, tag.id)
            for exercise in exercises
            for tag in exercise.tags.all()
        ])

        with self.assertNumQueries(1):
            exercise_ids_and_tags = sorted(get_exercise_ids_and_tags(self.course))

        self.assertListEqual(expected, exercise_ids_and_tags)

    def test_get_exercise_ids_by_tag_name(self):
        tags = BuildTags().for_course(self.course).with_names(*self.tag_names).build()
        print(tags)
        exercise_ids_and_tags = [
            (1, tags[0].id), (1, tags[1].id),
            (2, tags[0].id), (2, tags[2].id),
            (3, tags[2].id),
        ]

        expected = {
            tags[0].name: {1, 2},
            tags[1].name: {1},
            tags[2].name: {2, 3},
        }

        with self.assertNumQueries(0):
            exercise_ids_by_tag_name = get_exercise_ids_by_tag_name(exercise_ids_and_tags, tags)

        self.assertDictEqual(expected, exercise_ids_by_tag_name)

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

        self.assertDictEqual(expected, exercise_ids_by_tag_group)


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
            self.assertDictEqual(expected, count_total_exercises_by_tag_group(exercise_ids_by_tag_group))

    def test_get_points_by_exercise_id(self):
        BuildTags().for_course(self.other_course).with_names(*self.tag_names, 'choice').build()
        BuildTags().for_course(self.course).with_names(*self.tag_names, 'choice').build()

        tag_groups = ['python/if', 'python/while', 'python/while/choice', 'python/choice', 'design', 'design/choice']
        exercises = (
            BuildExercises()
                .for_course(self.other_course)
                .for_tag_groups(tag_groups)
                .build()
        )
        exercises += (
            BuildExercises()
                .for_course(self.course)
                .for_tag_groups(tag_groups)
                .build()
        )

        build_submissions_for_student = (
            BuildTelemetryDatas()
                .by_author(self.student)
                .for_exercises(exercises)
                .except_those_in_the_tag_groups(['python/if'])
        )
        build_submissions_for_other_student = (
            BuildTelemetryDatas()
                .by_author(self.other_student)
                .for_exercises(exercises)
                .except_those_in_the_tag_groups(['python/if'])
        )
        last_points = 0.5
        for points in [0.3, 0.7, last_points]:
            build_submissions_for_student.with_points(points).build()
            build_submissions_for_other_student.with_points(points).build()

        exercises_with_points = [
            exercise
            for exercise in build_submissions_for_student.exercises
            if exercise.course == self.course
        ]
        expected = {
            exercise.id: last_points
            for exercise in exercises_with_points
        }

        points_by_exercise_id = get_points_by_exercise_id(self.student, self.course)
        self.assertDictEqual(expected, points_by_exercise_id)

    def test_sum_points_for_tag_tree(self):
        exercise_ids_by_tag_group = {
            'python': {1, 2, 3, 4, 5},
            'python/if': {1, 2},
            'python/while': {3, 4},
            'design': set(),
        }

        points_by_exercise_id = {i: i / 10 for i in range(10)}

        expected = {
            'python': 1.5,
            'python/if': 0.3,
            'python/while': 0.7,
            'design': 0,
        }

        points_by_tag_group = sum_points_by_tag_group(points_by_exercise_id, exercise_ids_by_tag_group)
        self.assertDictAlmostEqual(expected, points_by_tag_group, places=3)

    def assertDictAlmostEqual(self, d1, d2, places=None, msg=None, delta=None):
        self.assertEqual(len(d1), len(d2), msg)
        for key in d1:
            self.assertTrue(key in d2, msg)
            self.assertAlmostEqual(d1[key], d2[key], places, msg, delta)
