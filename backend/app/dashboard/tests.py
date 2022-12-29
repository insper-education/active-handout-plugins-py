from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied

from core.models import Student, Instructor, Exercise, ExerciseTag, Course
from dashboard.views import student_dashboard_fragment
from dashboard.query import count_total_exercises_by_tag, list_tags_from_tree


class DashboardTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.student = Student.objects.create_user(username='gandalf', email='thegray@middleearth.nz', password='you-shall-not-pass')
        self.other_student = Student.objects.create_user(username='saruman', email='thewhite@middleearth.nz', password='the-hour-is-later-than-you-think')
        self.instructor = Instructor.objects.create_user(username='tolkien', email='jrrt@ox.ac.uk', password='not-all-those-who-wander-are-lost')

    def test_student_cant_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/student/{self.student.id}')
        request.user = self.other_student

        self.assertRaises(PermissionDenied, student_dashboard_fragment, request, self.student.id)

    def test_student_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/student/{self.student.id}')
        request.user = self.student

        assert student_dashboard_fragment(request, self.student.id) is not None

    def test_instructor_can_get_other_students_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/student/{self.student.id}')
        request.user = self.instructor

        assert student_dashboard_fragment(request, self.student.id) is not None

    def test_instructor_can_get_own_dashboard(self):
        request = self.factory.get(f'/dashboard/fragments/student/{self.instructor.id}')
        request.user = self.instructor

        assert student_dashboard_fragment(request, self.instructor.id) is not None


class QueryTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course')
        self.other_course = Course.objects.create(name='Not So Awesome Course')
        self.complex_tree = {
            'python': {
                'if': 'If',
                'while': 'While',
            },
            'design': {
                'frontend': {
                    'html': 'HTML',
                    'css': 'CSS',
                },
                'user-centered': 'User-Centered Design'
            }
        }
        self.simple_tree = {
            'python': 'Python',
        }

    def test_count_total_exercises_for_tag_tree(self):
        total_per_group = 4
        tag_groups = ['python/if', 'python/while', 'design/frontend', 'design/frontend/css', 'design/user-centered']
        for i, tag_group in enumerate(tag_groups):
            for j in range(total_per_group):
                exercise = Exercise.objects.create(course=self.course, slug=f'Exercise {i * total_per_group + j}')
                tags = tag_group.split('/')
                for tag_name in tags:
                    tag, _ = ExerciseTag.objects.get_or_create(course=self.course, name=tag_name)
                    exercise.tags.add(tag)
                exercise.save()

        expected = {
            'python': total_per_group * 2,
            'python/if': total_per_group,
            'python/while': total_per_group,
            'design': total_per_group * 2,
            'design/frontend': total_per_group * 2,
            'design/frontend/html': 0,
            'design/frontend/css': total_per_group,
            'design/user-centered': total_per_group,
        }

        # with self.assertNumQueries(6):
        assert expected == count_total_exercises_by_tag(self.course, self.complex_tree)

    def test_ignore_exercises_from_other_course_in_count(self):
        total_per_course = 4
        for course in [self.course, self.other_course]:
            for i in range(total_per_course):
                exercise = Exercise.objects.create(course=course, slug=f'Exercise {i}')
                tag, _ = ExerciseTag.objects.get_or_create(course=course, name='python')
                exercise.tags.add(tag)
                exercise.save()

        expected = {
            'python': total_per_course,
        }

        assert expected == count_total_exercises_by_tag(self.course, self.simple_tree)

    def test_list_tags_from_tree(self):
        expected = sorted(
            ['python', 'if', 'while', 'design', 'frontend', 'html', 'css', 'user-centered']
        )
        assert expected == sorted(list_tags_from_tree(self.complex_tree))
