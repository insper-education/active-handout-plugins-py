from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student, Instructor, Course, CourseClass, Exercise, ExerciseTag, TelemetryData


admin.site.register(Student, UserAdmin)
admin.site.register(Instructor, UserAdmin)
admin.site.register(Course)
admin.site.register(CourseClass)
admin.site.register(Exercise)
admin.site.register(ExerciseTag)
admin.site.register(TelemetryData)
