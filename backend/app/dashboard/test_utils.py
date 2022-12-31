from itertools import count

from core.models import (Course, Exercise, ExerciseTag, Instructor, Student,
                         TelemetryData, User)


class Builder:
    def __init__(self, *required_fields, optional=None):
        self.__required_fields = list(required_fields)
        self.__optional_fields = list(optional or [])
        self.__fields = self.__required_fields + self.__optional_fields
        for field in self.__fields:
            setattr(self, field, None)

    def build(self):
        for field in self.__required_fields:
            assert getattr(self, field), f'Field {field} is required for builder {self.getClass()}'

        return self.do_build()

    def do_build(self):
        raise NotImplementedError()

    def called(self, name):
        if 'name' in self.__fields:
            self.name = name
            return self
        raise NotImplementedError()

    def _field_dict(self):
        return {
            field: getattr(self, field)
            for field in self.__fields
            if getattr(self, field) is not None
        }

    def __getattr__(self, name):
        with_str = 'with_'
        field_name = name[len(with_str):]
        if name.startswith(with_str) and field_name in self.__fields:
            def with_field(value):
                setattr(self, field_name, value)
                # Return self to continue the chain
                return self
            return with_field


class BuildACourse(Builder):
    def __init__(self):
        super().__init__('name')

    def do_build(self) -> Course:
        return Course.objects.create(name=self.name)


class BuildAUser(Builder):
    def __init__(self, UserModel=User):
        super().__init__('username', 'email', 'password', optional=['first_name', 'last_name', 'nickname', 'picture', 'is_staff'])
        self.UserModel = UserModel

    def called(self, name):
        self.first_name = name
        return self

    def do_build(self) -> Course:
        return self.UserModel.objects.create_user(**self._field_dict())


class BuildAStudent(BuildAUser):
    def __init__(self):
        super().__init__(Student)


class BuildAnInstructor(BuildAUser):
    def __init__(self):
        super().__init__(Instructor)


class BuildTags(Builder):
    def __init__(self):
        super().__init__('course')

    def for_course(self, course):
        return self.with_course(course)

    def with_names(self, *tag_names):
        self.tag_names = tag_names
        return self

    def do_build(self) -> list[ExerciseTag]:
        assert self.tag_names

        tags = [
            ExerciseTag(name=tag_name, course=self.course)
            for tag_name in self.tag_names
        ]
        return ExerciseTag.objects.bulk_create(tags)


class BuildAnExercise(Builder):
    _exercise_counter = count(1)

    def __init__(self):
        super().__init__('course', 'slug', optional=['enabled'])
        self._slug = ''
        self.tags = []

    def for_course(self, course):
        return self.with_course(course)

    def with_slug(self, slug):
        self._slug = slug
        return self

    @property
    def slug(self):
        if not self._slug:
            self._slug = f'exercise-{next(self._exercise_counter)}'
        return self._slug

    @slug.setter
    def slug(self, new_slug):
        self._slug = new_slug

    def with_tags(self, tags: list[str | ExerciseTag]):
        self.tags = tags
        return self

    def do_build(self) -> Exercise:
        exercise = Exercise.objects.create(**self._field_dict())

        for tag in self.tags:
            if isinstance(tag, str):
                tag, _ = ExerciseTag.objects.get_or_create(course=self.course, name=tag)
            exercise.tags.add(tag)
        exercise.save()

        return exercise


class BuildExercises(Builder):
    def __init__(self):
        super().__init__('course', 'tag_groups')
        self.__exercises_per_group = 1

    def for_course(self, course):
        return self.with_course(course)

    def for_tag_groups(self, tag_groups):
        return self.with_tag_groups(tag_groups)

    def each_group_with(self, exercises_per_group):
        self.__exercises_per_group = exercises_per_group
        return self

    def do_build(self):
        exercises = []
        for tag_group in self.tag_groups:
            tags = tag_group.split('/')
            for _ in range(self.__exercises_per_group):
                exercises.append(
                    BuildAnExercise()
                        .for_course(self.course)
                        .with_tags(tags)
                        .build()
                )
        return exercises


class BuildATelemetryData(Builder):
    def __init__(self):
        super().__init__('author', 'exercise', 'points', 'log', optional=['submission_date', 'last'])
        self.log = '{}'

    def by_author(self, author):
        return self.with_author(author)

    def for_exercise(self, exercise):
        return self.with_exercise(exercise)

    def do_build(self) -> TelemetryData:
        return TelemetryData.objects.create(**self._field_dict())


# DATAS... ARGH :(
class BuildTelemetryDatas(Builder):
    def __init__(self):
        super().__init__('author', 'exercises', 'points')

    def by_author(self, author):
        return self.with_author(author)

    def for_exercises(self, exercises):
        return self.with_exercises(exercises)

    def for_all_exercises_of(self, course):
        return self.with_exercises(Exercise.objects.filter(course=course))

    def except_those_in_the_tag_groups(self, tag_groups):
        for tag_group in tag_groups:
            tags = tag_group.split('/')
            self.exercises = [
                exercise
                for exercise in self.exercises
                if not all(tag.name in tags for tag in exercise.tags.all())
            ]
        return self

    def do_build(self) -> list[TelemetryData]:
        return [
            BuildATelemetryData()
                .for_exercise(exercise)
                .by_author(self.author)
                .with_points(self.points)
                .build()
            for exercise in self.exercises
        ]
