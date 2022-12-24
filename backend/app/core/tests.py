from django.utils.translation import gettext as _
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from core.models import Instructor, User, Exercise, Course, ExerciseTag, Student, TelemetryData
from core.views import ensure_tags_equal, telemetry_data, get_all_answers


class StudentAndInstructorTests(TestCase):
    def test_instructor_always_staff(self):
        self.prof1 = Instructor.objects.create_user(
            username='prof12',
            password='12'
        )
        assert self.prof1.is_staff == True


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
        tags = sorted([tag.name for tag in exercise.tags.all()])
        assert tags == expected_tags, f'Tags are different than expected. Expected {expected_tags}. Got {tags}.'

    def test_ensure_tags_for_existing_exercise(self):
        old_tags = ['code', 'loop']
        expected_tags = ['code', 'recursion', 'impossible']

        exercise = Exercise.objects.create(course=self.course, slug='very-hard-challenge')
        for tag_name in old_tags:
            tag = ExerciseTag.objects.create(course=self.course, name=tag_name)
            exercise.tags.add(tag)

        ensure_tags_equal(exercise, expected_tags)

        expected_tags = sorted(expected_tags)
        tags = sorted([tag.name for tag in exercise.tags.all()])
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

        for st in self.students:
            for ex in self.exercises:
                TelemetryData.objects.create(author=st, exercise=ex, points=0, log="NO")
                TelemetryData.objects.create(author=st, exercise=ex, points=1, log="OK")


    def test_student_cant_get_answers(self):
        request = self.factory.get(f'/api/telemetry/answers/{self.course.name}/{self.exercises[0].slug}')
        force_authenticate(request, user=self.students[0])
        response = get_all_answers(request, self.course.name, self.exercises[0].slug)
        assert response.status_code == 403
    
    def test_instructors_can_get_answers(self):
        request = self.factory.get(f'/api/telemetry/answers/{self.course.name}/{self.exercises[0].slug}')
        force_authenticate(request, user=self.instructor)
        response = get_all_answers(request, self.course.name, self.exercises[0].slug)
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
        request = self.factory.get(f'/api/telemetry/answers/{self.course.name}/{self.exercises[0].slug}')
        force_authenticate(request, user=self.instructor)
        response = get_all_answers(request, self.course.name, self.exercises[0].slug)
        assert response.status_code == 200
        author_exercise_pairs = set()
        for it in response.data:
            assert it["points"] == 1 and it["log"] != "NO"
            pair = (it["author"]["username"], it["exercise"]["course"], it["exercise"]["slug"])
            assert pair not in author_exercise_pairs
            author_exercise_pairs.add(pair)
