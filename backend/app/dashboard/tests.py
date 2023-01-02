import datetime

from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from dashboard.query import (count_total_exercises_by_tag_group, get_all_tags,
                             get_exercise_count_by_tag_slug_and_date,
                             get_exercise_ids_and_tags,
                             get_exercise_ids_by_date,
                             get_exercise_ids_by_tag_group,
                             get_exercise_ids_by_tag_slug, get_exercises_by_id,
                             get_points_by_exercise_id, setup_tag_names,
                             sum_points_by_tag_group)
from dashboard.tag_tree import TagTree, TagTreeNode
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
        self.tag_tree = TagTree.from_yaml_repr([
            {
                'python': ['if', 'while']
            },
            'design',
        ])
        self.tag_slugs = self.tag_tree.get_tags()

    def test_get_all_tags(self):
        BuildTags().for_course(self.other_course).with_slugs(*self.tag_slugs).build()
        course_tags = BuildTags().for_course(self.course).with_slugs(*self.tag_slugs).build()
        course_tags = sorted(course_tags, key=lambda t: t.slug)

        with self.assertNumQueries(1):
            self.assertQuerysetEqual(
                get_all_tags(self.course, self.tag_slugs).order_by('slug'),
                course_tags
            )

    def test_get_exercise_ids_and_tags(self):
        BuildTags().for_course(self.other_course).with_slugs(*self.tag_slugs).build()
        BuildTags().for_course(self.course).with_slugs(*self.tag_slugs).build()

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

    def test_get_exercise_ids_by_tag_slug(self):
        tags = BuildTags().for_course(self.course).with_slugs(*self.tag_slugs).build()
        print(tags)
        exercise_ids_and_tags = [
            (1, tags[0].id), (1, tags[1].id),
            (2, tags[0].id), (2, tags[2].id),
            (3, tags[2].id),
        ]

        expected = {
            tags[0].slug: {1, 2},
            tags[1].slug: {1},
            tags[2].slug: {2, 3},
        }

        with self.assertNumQueries(0):
            exercise_ids_by_tag_slug = get_exercise_ids_by_tag_slug(exercise_ids_and_tags, tags)

        self.assertDictEqual(expected, exercise_ids_by_tag_slug)

    def test_get_exercise_ids_by_tag_group(self):
        exercise_ids_by_tag_slug = {
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
            exercise_ids_by_tag_group = get_exercise_ids_by_tag_group(self.tag_tree, exercise_ids_by_tag_slug)

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
        BuildTags().for_course(self.other_course).with_slugs(*self.tag_slugs, 'choice').build()
        BuildTags().for_course(self.course).with_slugs(*self.tag_slugs, 'choice').build()

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

        build_submissions = (
            BuildTelemetryDatas()
                .for_exercises(exercises)
                .except_those_in_the_tag_groups(['python/if'])
        )

        last_points = 0.5
        for points in [0.3, 0.7, last_points]:
            build_submissions.by_author(self.student).with_points(points).build()
            build_submissions.by_author(self.other_student).with_points(points).build()

        exercises_with_points = [
            exercise
            for exercise in build_submissions.exercises
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

    def test_get_exercise_ids_by_date(self):
        start_date = (2022, 8, 1)
        end_date = (2022, 12, 1)
        self.course = (
            BuildACourse()
                .called('Current Course')
                .starting_at(*start_date)
                .ending_at(*end_date)
                .build()
        )
        self.other_course = (
            BuildACourse()
                .called('Other Current Course')
                .starting_at(*start_date)
                .ending_at(*end_date)
                .build()
        )

        tag_groups = ['python', 'java', 'c', 'c++']
        exercises_in_other_course = (
            BuildExercises()
                .for_course(self.other_course)
                .for_tag_groups(tag_groups)
                .each_group_with(5)
                .build()
        )
        exercises_in_course = (
            BuildExercises()
                .for_course(self.course)
                .for_tag_groups(tag_groups)
                .each_group_with(5)
                .build()
        )
        all_exercises = exercises_in_other_course + exercises_in_course

        exercises_by_date_and_student = {
            self.student: {
                (2022, 7, 28): all_exercises[::3],
                start_date: all_exercises[::2],
                (2022, 9, 6): all_exercises[::4],
                (2022, 11, 30): all_exercises,
                end_date: all_exercises,
                (2022, 12, 3): all_exercises[::5],
            },
            self.other_student: {
                (2022, 7, 20): all_exercises,
                start_date: all_exercises[::4],
                (2022, 10, 5): all_exercises[::5],
                end_date: all_exercises[::2],
                (2022, 12, 5): all_exercises,
            },
        }

        for student, exercises_by_date in exercises_by_date_and_student.items():
            for date, exercises in exercises_by_date.items():
                # Create 3 submissions per exercise
                for _ in range(3):
                    (
                        BuildTelemetryDatas()
                            .by_author(student)
                            .for_exercises(exercises)
                            .submitted_on(*date)
                            .build()
                    )

        expected_list = set(
            (datetime.datetime(*date, tzinfo=datetime.timezone.utc).date(), exercise.id)
            for date, exercises in exercises_by_date_and_student[self.student].items()
            for exercise in exercises
            if start_date <= date <= end_date and exercise.course == self.course
        )

        expected_exercise_ids_by_date = {}
        expected_exercise_count_by_tag_and_date = {}
        exercises_by_id = get_exercises_by_id(self.course)
        for date, exercise_id in expected_list:
            expected_exercise_ids_by_date.setdefault(date, []).append(exercise_id)
            for tag in exercises_by_id[exercise_id].tags.all():
                tag_counts = expected_exercise_count_by_tag_and_date.setdefault(tag.slug, {})
                tag_counts[date] = tag_counts.get(date, 0) + 1
        for date, exercise_ids in expected_exercise_ids_by_date.items():
            expected_exercise_ids_by_date[date] = sorted(exercise_ids)

        with self.assertNumQueries(1):
            exercise_ids_by_date = get_exercise_ids_by_date(self.student, self.course)
            for date, exercise_ids in exercise_ids_by_date.items():
                exercise_ids_by_date[date] = sorted(exercise_ids)
            self.assertDictEqual(expected_exercise_ids_by_date, exercise_ids_by_date)

        with self.assertNumQueries(0):
            counts = get_exercise_count_by_tag_slug_and_date(exercise_ids_by_date, exercises_by_id)
            self.assertDictEqual(expected_exercise_count_by_tag_and_date, counts)


    def test_get_exercise_ids_by_date_with_missing_start_date(self):
        end_date = (2022, 12, 1)
        self.course = (
            BuildACourse()
                .called('Current Course')
                .ending_at(*end_date)
                .build()
        )
        self.other_course = (
            BuildACourse()
                .called('Other Current Course')
                .ending_at(*end_date)
                .build()
        )

        exercise_ids_by_date = get_exercise_ids_by_date(self.student, self.course)
        with self.assertNumQueries(0):
            self.assertDictEqual({}, exercise_ids_by_date)

    def test_get_exercise_ids_by_date_with_missing_end_date(self):
        start_date = (2022, 8, 1)
        self.course = (
            BuildACourse()
                .called('Current Course')
                .starting_at(*start_date)
                .build()
        )
        self.other_course = (
            BuildACourse()
                .called('Other Current Course')
                .starting_at(*start_date)
                .build()
        )

        exercise_ids_by_date = get_exercise_ids_by_date(self.student, self.course)
        with self.assertNumQueries(0):
            self.assertDictEqual({}, exercise_ids_by_date)

    def test_get_exercise_ids_by_date_with_both_missing_dates(self):
        exercise_ids_by_date = get_exercise_ids_by_date(self.student, self.course)
        with self.assertNumQueries(0):
            self.assertDictEqual({}, exercise_ids_by_date)

    def test_setup_tag_names(self):
        tags = BuildTags().for_course(self.course).with_slugs(*self.tag_tree.get_tags()).build()
        for tag in tags:
            tag.name = tag.slug.title()
            tag.save()

        setup_tag_names(self.tag_tree, tags)

        for node in self.tag_tree.get_nodes():
            self.assertEqual(node.slug.title(), node.name)
            self.assertNotEqual(node.slug, node.name)

    def test_get_exercises_by_id(self):
        tag_groups = ['python', 'java', 'c', 'c++']
        BuildExercises().for_course(self.other_course).for_tag_groups(tag_groups).each_group_with(5).build()
        exercises = BuildExercises().for_course(self.course).for_tag_groups(tag_groups).each_group_with(5).build()

        expected = {exercise.id: exercise for exercise in exercises}

        # One query for the exercise list and another for prefetching the tags
        with self.assertNumQueries(2):
            exercises_by_id = get_exercises_by_id(self.course)
            self.assertDictEqual(expected, exercises_by_id)
            for exercise in exercises_by_id.values():
                # Force query if not prefetch
                for tag in exercise.tags.all():
                    tag.slug


    def assertDictAlmostEqual(self, d1, d2, places=None, msg=None, delta=None):
        self.assertEqual(len(d1), len(d2), msg)
        for key in d1:
            self.assertTrue(key in d2, msg)
            self.assertAlmostEqual(d1[key], d2[key], places, msg, delta)


class TagTreeTest(TestCase):
    def test_create_from_yaml_repr(self):
        yaml_repr = [
            {
                'python': [
                    'if',
                    {
                        'while': ['intro', 'algorithms'],
                    },
                ]
            },
            'design',
        ]

        tree_from_repr = TagTree.from_yaml_repr(yaml_repr)
        expected = TagTree()
        expected.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        self.assertEqual(expected, tree_from_repr)

    def test_tag_trees_equal(self):
        tree1 = TagTree()
        tree1.root.children=[
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        tree2 = TagTree()
        tree2.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        self.assertEqual(tree1, tree2)

    def test_tag_trees_different_if_not_same_groups(self):
        tree1 = TagTree()
        tree1.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        tree2 = TagTree()
        tree2.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        self.assertNotEqual(tree1, tree2)

    def test_tag_trees_different_if_missing_sub_tree(self):
        tree1 = TagTree()
        tree1.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        tree2 = TagTree()
        tree2.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
            ]),
            TagTreeNode('design', 'design'),
        ]

        self.assertNotEqual(tree1, tree2)

    def test_tag_trees_different_if_not_same_order(self):
        tree1 = TagTree()
        tree1.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        tree2 = TagTree()
        tree2.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
                TagTreeNode('if', 'python/if'),
            ]),
            TagTreeNode('design', 'design'),
        ]

        self.assertNotEqual(tree1, tree2)

    def test_get_tags_from_tree(self):
        tree = TagTree()
        tree.root.children = [
            TagTreeNode('python', 'python', [
                TagTreeNode('if', 'python/if'),
                TagTreeNode('while', 'python/while', [
                    TagTreeNode('intro', 'python/while/intro'),
                    TagTreeNode('algorithms', 'python/while/algorithms'),
                ]),
            ]),
            TagTreeNode('design', 'design'),
        ]

        expected = ['algorithms', 'design', 'if', 'intro', 'python', 'while']
        self.assertListEqual(expected, sorted(tree.get_tags()))

    def test_get_nodes(self):
        intro_node = TagTreeNode('intro', 'python/while/intro')
        algorithms_node = TagTreeNode('algorithms', 'python/while/algorithms')
        if_node = TagTreeNode('if', 'python/if')
        while_node = TagTreeNode('while', 'python/while', [
            intro_node,
            algorithms_node,
        ])
        python_node = TagTreeNode('python', 'python', [
            if_node,
            while_node,
        ])
        design_node = TagTreeNode('design', 'design')

        tree = TagTree()
        tree.root.children = [
            python_node,
            design_node,
        ]

        expected = [python_node, if_node, while_node, intro_node, algorithms_node, design_node]
        self.assertListEqual(expected, tree.get_nodes())

