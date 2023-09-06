from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student, Instructor, Course, CourseClass, Exercise, ExerciseTag, TelemetryData

class TelemetryDataAdmin(admin.ModelAdmin):
    list_filter = ("author", "exercise")
    readonly_fields = ('solution',)
    
admin.site.register(Student, UserAdmin)
admin.site.register(Instructor, UserAdmin)
admin.site.register(Course)
admin.site.register(CourseClass)
admin.site.register(Exercise)
admin.site.register(ExerciseTag)
admin.site.register(TelemetryData, TelemetryDataAdmin)


    

