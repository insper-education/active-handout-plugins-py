from urllib.parse import quote
from datetime import timedelta

from core.models import (Course, Exercise, ExerciseTag, Instructor, Student,
                         TelemetryData, User)
from core.shortcuts import redirect
from core.views import (disable_exercise, enable_exercise, ensure_tags_equal,
                        exercise_list, get_all_students_answers, get_answers,
                        login_request, telemetry_data, update_tag_names)
from django.core.exceptions import DisallowedRedirect
from django.test import RequestFactory, TestCase
from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate


class StudentAndInstructorTests(TestCase):
    def test_instructor_always_staff(self):
        self.prof1 = Instructor.objects.create_user(
            username='prof12',
            password='12'
        )
        assert self.prof1.is_staff == True


class AuthTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='gandalf', email='thegray@middleearth.nz', password='you-shall-not-pass')
        self.token = Token.objects.create(user=self.user)

    def test_redirects_to_vscode_if_logged_in(self):
        next = 'vscode://domain.extension'
        request = self.factory.get(f'/api/login?next={next}')
        request.user = self.user
        request.session = {}

        response = login_request(request)
        assert response.url == f'{next}?token={self.token}'

    def test_doesnt_redirect_to_unauthorized_scheme(self):
        next = 'wrong://domain.extension'
        request = self.factory.get(f'/api/login?next={next}')
        request.user = self.user
        request.session = {}

        self.assertRaises(DisallowedRedirect, login_request, request)


class TelemetryDataTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = APIRequestFactory()

    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course 2022')
        self.user = User.objects.create_user(username='bill.doors', password='billy123')

    def test_ensure_tags_for_new_exercise(self):
        expected_tags = ['code', 'recursion', 'impossible']
        exercise = Exercise.objects.create(course=self.course, slug='very-hard-challenge')
        ensure_tags_equal(exercise, expected_tags)

        expected_tags = sorted(expected_tags)
        tags = sorted([tag.slug for tag in exercise.tags.all()])
        assert tags == expected_tags, f'Tags are different than expected. Expected {expected_tags}. Got {tags}.'

    def test_ensure_tags_for_existing_exercise(self):
        old_tags = ['code', 'loop']
        expected_tags = ['code', 'recursion', 'impossible']

        exercise = Exercise.objects.create(course=self.course, slug='very-hard-challenge')
        for tag_slug in old_tags:
            tag = ExerciseTag.objects.create(course=self.course, slug=tag_slug)
            exercise.tags.add(tag)

        ensure_tags_equal(exercise, expected_tags)

        expected_tags = sorted(expected_tags)
        tags = sorted([tag.slug for tag in exercise.tags.all()])
        assert tags == expected_tags, f'Tags are different than expected. Expected {expected_tags}. Got {tags}.'

    def test_new_telemetry_data_creates_course_and_exercise(self):
        data = {
            "exercise": {
                "course": "New Course 2023",
                "slug": "very-simple-exercise",
                "tags": ["code", "if", "easy"],
            },
            "points": 0.5,
            "log": {"answer": "right", "expected": "wrong"},
        }

        request = self.factory.post('/api/telemetry/', data, format='json')
        force_authenticate(request, user=self.user)
        response = telemetry_data(request)

        assert response.status_code == 200, f'Wrong status code. Expected 200, got {response.status_code}'
        assert Course.objects.filter(name=data['exercise']['course']).exists()
        assert Exercise.objects.filter(slug=data['exercise']['slug']).exists()


class AnswerEndPointTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = APIRequestFactory()

    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course 2022')
        self.exercises = [
            Exercise.objects.create(course=self.course, slug=f'ex{i}')
            for i in range(10)
        ]
        self.instructor = Instructor.objects.create_user(username='igor', password='igorigor', is_staff=True)
        self.students = [
            Student.objects.create_user(f'student{i}', password=f'oi{i}')
            for i in range(3)
        ]

        for st in self.students + [self.instructor]:
            for ex in self.exercises:
                for answer, points, dt in [
                    ('NO', 0, -2),
                    ('NO', 0, -1),
                    ('OK', 1, 1),
                ]:
                    submission_date = timezone.now() + timedelta(hours=dt)
                    TelemetryData.objects.create(author=st, exercise=ex, points=points, log=answer, submission_date=submission_date)

    def test_student_cant_get_all_students_answers(self):
        request = self.factory.get(f'/api/telemetry/answers/', {'course_name': self.course.name,
                                                                'exercise_slug': self.exercises[0].slug})
        force_authenticate(request, user=self.students[0])
        response = get_all_students_answers(request)
        assert response.status_code == 403
    
    def test_instructors_can_get_all_students_answers(self):
        request = self.factory.get(f'/api/telemetry/answers/', {'course_name': self.course.name,
                                                                'exercise_slug': self.exercises[0].slug})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
    
    def test_get_student_answers(self):
        student = self.students[0]
        exercise = self.exercises[0]
        request = self.factory.get(f'/api/telemetry/answers/', {'course_name': self.course.name,
                                                                'exercise_slug': exercise.slug})
        force_authenticate(request, user=student)
        response = get_answers(request)
        assert response.status_code == 200

        for it in response.data:
            assert it["author"]["username"] == student.username
            assert it["exercise"]["course"] == self.course.name
            assert it["exercise"]["slug"] == exercise.slug

    def test_get_student_answers_for_multiple_exercises(self):
        student = self.students[0]
        request = self.factory.get(f'/api/telemetry/answers/', {'course_name': self.course.name,
                                                                'exercise_slug': ','.join(e.slug for e in self.exercises)})
        force_authenticate(request, user=student)
        response = get_answers(request)
        assert response.status_code == 200

        assert len(response.data) == len(self.exercises)
        for it in response.data:
            assert it["author"]["username"] == student.username
            assert it["exercise"]["course"] == self.course.name
    
    def test_exercise_course_with_slash(self):
        course = Course.objects.create(name="course/slash")
        ex_with_slash = Exercise.objects.create(course=course, slug="a/b/c")
        course_name_quote = quote(course.name, safe='')
        ex_slug_quote = quote(ex_with_slash.slug, safe='')
                                  
        request = self.factory.get(f'/api/telemetry/answers/', {'course_name': course_name_quote,
                                                                'exercise_slug': ex_slug_quote})                               
        force_authenticate(request, user=self.instructor)
        response = get_answers(request)
        assert response.status_code == 200

    def test_adding_new_exercise_updates_last(self):
        st = self.students[0]
        ex = self.exercises[0]
        last_student0 = TelemetryData.objects.get(author=st, exercise=ex, last=True)
        new_last_student0 = TelemetryData.objects.create(author=st, exercise=ex, points=1, log="NEW")
        assert new_last_student0.last == True
        assert new_last_student0.log == "NEW"
        last_student0.refresh_from_db()
        assert last_student0.last == False

    def test_get_all_last_answers(self):
        request = self.factory.get(f'/api/telemetry/answers/all-students',
                                   {'course_name': self.course.name,
                                    'exercise_slug': self.exercises[0].slug})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == len(self.students) + 1  # Each student + instructor has at least 1 submission
        author_exercise_pairs = set()
        for it in response.data:
            assert it["points"] == 1 and it["log"] != "NO"
            pair = (it["author"]["username"], it["exercise"]["course"], it["exercise"]["slug"])
            assert pair not in author_exercise_pairs
            author_exercise_pairs.add(pair)
    
    def test_get_all_last_answers_before_now(self):
        request = self.factory.get(f'/api/telemetry/answers/all-students',
                                   {'course_name': self.course.name,
                                    'exercise_slug': self.exercises[0].slug,
                                    "before": timezone.now().isoformat()})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == len(self.students) + 1  # Each student + instructor has at least 1 submission and the last submission before now didn't pass
        author_exercise_pairs = set()
        for it in response.data:
            assert it["points"] == 0 and it["log"] == "NO"
            pair = (it["author"]["username"], it["exercise"]["course"], it["exercise"]["slug"])
            assert pair not in author_exercise_pairs
            author_exercise_pairs.add(pair)

    def test_get_all_answers(self):
        exercise = self.exercises[0]
        request = self.factory.get(f'/api/telemetry/answers/all-students', 
                                   {'course_name': self.course.name,
                                    'exercise_slug': exercise.slug,
                                    'all': 'true'})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == 3 * (len(self.students) + 1)  # Each student + instructor has 3 answers
        for it in response.data:
            assert it["exercise"]["course"] == self.course.name
            assert it["exercise"]["slug"] == exercise.slug
    
    def test_get_all_answers_before_date(self):
        exercise = self.exercises[0]
        request = self.factory.get(f'/api/telemetry/answers/all-students', 
                                   {'course_name': self.course.name,
                                    'exercise_slug': exercise.slug,
                                    'all': 'true',
                                    'before': timezone.now().isoformat()})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == 2 * (len(self.students) + 1)  # Each student + instructor has 3 answers, but only the first two were before now (the other is in the future)
        for it in response.data:
            assert it["exercise"]["course"] == self.course.name
            assert it["exercise"]["slug"] == exercise.slug
            assert it["log"] == "NO"
    
    def test_get_all_answers_for_multiple_exercises(self):
        request = self.factory.get(f'/api/telemetry/answers/all-students', 
                                   {'course_name': self.course.name,
                                    'exercise_slug': ','.join([e.slug for e in self.exercises]),
                                    'all': 'true'})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == 3 * (len(self.students) + 1) * len(self.exercises)  # Each student + instructor has 3 answers for each exercise
        for it in response.data:
            assert it["exercise"]["course"] == self.course.name
    
    def test_get_all_answers_for_multiple_exercises_before_date(self):
        request = self.factory.get(f'/api/telemetry/answers/all-students', 
                                   {'course_name': self.course.name,
                                    'exercise_slug': ','.join([e.slug for e in self.exercises]),
                                    'all': 'true',
                                    'before': timezone.now().isoformat()})
        force_authenticate(request, user=self.instructor)
        response = get_all_students_answers(request)
        assert response.status_code == 200
        assert len(response.data) == 2 * (len(self.students) + 1) * len(self.exercises)  # Each student + instructor has 3 answers for each exercise, but 1 is in the future
        for it in response.data:
            assert it["exercise"]["course"] == self.course.name


class RedirectTests(TestCase):
    def test_redirect_allows_vscode_scheme(self):
        response = redirect('vscode://domain.extension')
        assert response is not None

    def test_redirect_disallows_other_schemes(self):
        self.assertRaises(DisallowedRedirect, redirect, 'wrong://domain.extension')


class ExerciseListTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = APIRequestFactory()

    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course 2022')
        self.instructor = Instructor.objects.create_user(username='igor', password='igorigor', is_staff=True)
        self.student = Student.objects.create_user('student', password='oi')

    def test_create_exercises_that_didnt_exist(self):
        Exercise.objects.create(course=self.course, slug='ex1')
        tags_by_exercise_slug = {
            'ex1': ['tag1', 'tag2'],
            'ex2': ['tag2', 'tag3'],
        }
        request = self.factory.post(f'/api/exercises/{self.course.name}', {
            'page/url/': {
                slug: {
                    'slug': slug,
                    'tags': tags
                }
                for slug, tags in tags_by_exercise_slug.items()
            }
        }, format='json')

        force_authenticate(request, user=self.instructor)
        response = exercise_list(request, self.course.name)
        assert response.status_code == 200

        exercises_by_slug = {e.slug: e for e in Exercise.objects.filter(course=self.course)}
        for slug, expected_tags in tags_by_exercise_slug.items():
            exercise = exercises_by_slug[slug]
            tag_slugs = [t.slug for t in exercise.tags.all()]
            for expected_tag in expected_tags:
                assert expected_tag in tag_slugs

    def test_student_cant_create_exercises(self):
        request = self.factory.post(f'/api/exercises/{self.course.name}', {
            'page/url/': {
                'ex1': {
                    'slug': 'ex1',
                    'tags': [],
                }
            }
        }, format='json')

        force_authenticate(request, user=self.student)
        response = exercise_list(request, self.course.name)
        assert response.status_code == 403


class EnableDisableExercise(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = APIRequestFactory()

    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course 2022')
        self.exercise_enabled = Exercise.objects.create(course=self.course, slug='ex1')
        self.exercise_disabled = Exercise.objects.create(course=self.course, slug='ex2', enabled=False)
        self.instructor = Instructor.objects.create_user(username='igor', password='igorigor', is_staff=True)
        self.student = Student.objects.create_user('student', password='oi')

    def test_enable_exercise(self):
        request = self.factory.get(f'/api/exercises/{self.course.name}/{self.exercise_disabled.slug}/enable')
        force_authenticate(request, user=self.instructor)
        response = enable_exercise(request, self.course.name, self.exercise_disabled.slug)
        assert response.status_code == 200
        self.exercise_disabled.refresh_from_db()
        assert self.exercise_disabled.enabled == True

    def test_disable_exercise(self):
        request = self.factory.get(f'/api/exercises/{self.course.name}/{self.exercise_enabled.slug}/disable')
        force_authenticate(request, user=self.instructor)
        response = disable_exercise(request, self.course.name, self.exercise_enabled.slug)
        assert response.status_code == 200
        self.exercise_enabled.refresh_from_db()
        assert self.exercise_enabled.enabled == False

    def test_student_cant_enable_disable_exercise(self):
        request = self.factory.get(f'/api/exercises/{self.course.name}/{self.exercise_enabled.slug}/disable')
        force_authenticate(request, user=self.student)
        response = disable_exercise(request, self.course.name, self.exercise_enabled.slug)
        assert response.status_code == 403
        self.exercise_enabled.refresh_from_db()
        assert self.exercise_enabled.enabled == True

        request = self.factory.get(f'/api/exercises/{self.course.name}/{self.exercise_disabled.slug}/enable')
        force_authenticate(request, user=self.student)
        response = enable_exercise(request, self.course.name, self.exercise_disabled.slug)
        assert response.status_code == 403
        self.exercise_disabled.refresh_from_db()
        assert self.exercise_disabled.enabled == False

    def test_submitting_to_disabled_exercise_fails(self):
        data = {
            "exercise": {
                "course": self.course.name,
                "slug": self.exercise_disabled.slug,
                "tags": [],
            },
            "points": 0.5,
            "log": "OK"
        }

        request = self.factory.post('/api/telemetry/', data, format='json')
        force_authenticate(request, user=self.student)
        response = telemetry_data(request)
        assert response.status_code == 403


class TagsTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = APIRequestFactory()

    def setUp(self):
        self.course = Course.objects.create(name='Awesome Course 2022')
        self.instructor = Instructor.objects.create_user(username='igor', password='igorigor', is_staff=True)
        self.student = Student.objects.create_user('student', password='oi')

    def test_update_tag_names(self):
        slugs_and_names = [
            ('ex1', 'Exercise 1'),
            ('ex2', None),
            ('ex3', 'ex3'),
        ]
        ExerciseTag.objects.bulk_create([ExerciseTag(slug=slug, name=name, course=self.course) for slug, name in slugs_and_names])

        request = self.factory.post(f'/api/tags/{self.course.name}/names', {
            'ex2': 'Exercise 2',
            'ex3': 'Exercise 3',
        }, format='json')

        force_authenticate(request, user=self.instructor)
        response = update_tag_names(request, self.course.name)
        assert response.status_code == 200

        for i in range(1, 4):
            tag = ExerciseTag.objects.get(course=self.course, slug=f'ex{i}')
            assert tag.name == f'Exercise {i}'

    def test_update_tag_shouldnt_create_tags(self):
        tag_slug = 'oops'
        request = self.factory.post(f'/api/tags/{self.course.name}/names', {
            tag_slug: "Exercise that doesn't exist",
        }, format='json')

        force_authenticate(request, user=self.instructor)
        response = update_tag_names(request, self.course.name)
        assert response.status_code == 200

        with self.assertRaises(ExerciseTag.DoesNotExist):
            ExerciseTag.objects.get(course=self.course, slug=tag_slug)

    def test_student_cant_create_exercises(self):
        request = self.factory.post(f'/api/tags/{self.course.name}/names', {
            'oops': "Exercise that doesn't exist",
        }, format='json')

        force_authenticate(request, user=self.student)
        response = exercise_list(request, self.course.name)
        assert response.status_code == 403
