from urllib.parse import unquote_plus
import json

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view


from core.models import Course, Exercise, TelemetryData, ExerciseTag
from dashboard.query import StudentStats
from django.db.models import Max


@api_view()
@login_required
def student_dashboard(request, course_name):
    student = request.user

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)

    tag_tree_yaml = json.loads(request.GET.get('tag-tree', '{}'))

    student_stats = StudentStats(student, course, tag_tree_yaml)

    return render(request, 'dashboard/student-dashboard.html', {
        'referer': request.META.get('HTTP_REFERER', ''),
        'course': course,
        'tags': student_stats.tags,
        'tag_tree': student_stats.tag_tree,
        'tag_stats': student_stats.stats_by_tag_group,
        'total_exercises': student_stats.total_exercises,
        'exercise_count_by_tag_slug_and_date': student_stats.exercise_count_by_tag_slug_and_date,
    })


@staff_member_required
@api_view()
@login_required
def instructor_courses(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/instructor-courses.html', {"courses": courses})


@staff_member_required
@api_view()
@login_required
def students_progress(request, course_name):

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    course_classes = course.courseclass_set.all().prefetch_related('students')
    course_classes_list = [
        {"name": course_class.name, "students": list(course_class.students.values_list('username', flat=True))}
        for course_class in course_classes
    ]

    exercises = Exercise.objects.filter(course=course)
    telemetry = list(TelemetryData.objects.filter(exercise__in=exercises).values('author__username', 'exercise__slug')
                     .annotate(max_points=Max('points')))

    tag_obj = {}
    for ex in exercises:
        for tag in list(ex.tags.all().values_list('name', flat=True)):
            tag_obj.setdefault(tag, [])
            tag_obj[tag].append(ex.slug)
    data = {}
    columns = set()
    for answer in telemetry:
        columns.add(answer['exercise__slug'])
        data.setdefault(answer['author__username'], {
                        "Name": answer['author__username']})
        data[answer['author__username']][answer['exercise__slug']
                                         ] = round(answer['max_points'], 1)
    sorted_columns = sorted(list(columns))
    columns_with_list = [*["Name"], *sorted_columns]

    data_list = sorted(list(data.values()), key=lambda d: d['Name'].lower())
    for d in data_list:
        print(d["Name"])

    return render(request, 'dashboard/instructor-progress.html',
                  {
                      'data': data_list,
                      'columns': columns_with_list,
                      'tags': tag_obj,
                      'course_classes': course_classes_list,
                  })
