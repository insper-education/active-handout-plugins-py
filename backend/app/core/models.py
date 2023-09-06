from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from django.utils.html import format_html


class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    picture = models.URLField(max_length=200, blank=True)


class StudentManager(UserManager):
    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = 'Student'


class InstructorManager(UserManager):
    def get_queryset(self):
        return User.objects.filter(is_staff=True)


class Instructor(User):
    objects = InstructorManager()

    class Meta:
        proxy = True
        verbose_name = 'Instructor'

    def save(self, *args, **kwargs):
        self.is_staff = True
        return super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class CourseClass(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"{self.name} ({self.course})"


class ExerciseTag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "slug"], name="unique_course_tag"
            ),
        ]

    def __str__(self):
        return f'[{self.slug}] {self.safe_name()} ({self.course})'

    def safe_name(self):
        if self.name:
            return self.name
        return self.slug


class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)
    tags = models.ManyToManyField(ExerciseTag)
    enabled = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "slug"], name="unique_course_exercise_slug"
            ),
        ]

    def __str__(self) -> str:
        return self.slug


class TelemetryData(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    points = models.FloatField()
    submission_date = models.DateTimeField(default=timezone.now)
    log = models.JSONField()
    last = models.BooleanField(default=True)

    def solution(self):
        formatted = ''
        log = self.log.get('student_input', {})
        print(log)

        template = '<pre style="padding: 0.5rem; margin-top: 0; border: 1px solid var(--primary); display: grid; overflow: auto;"><code>{content}</code></pre>'
        if type(log) == dict:
            for key, value in log.items():
                formatted += f'<h2>{key}</h2>'
                formatted += template.format(content=value)
        else:
            formatted += template.format(content=log)

        formatted = formatted.replace('{', '&#123;').replace('}', '&#125;')
        return format_html(formatted)


    def __str__(self) -> str:
        return f"{self.exercise} -> {self.author.username} ({self.submission_date})"
