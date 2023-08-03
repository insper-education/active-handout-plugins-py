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
    exercises = Exercise.objects.filter(course=course)
    tags = list(ExerciseTag.objects.filter(
        course=course).values_list('id', 'name'))
    tag_obj = {}
    for tag in tags:
        ex = list(Exercise.objects.filter(course=course,
                  tags=tag[0]).values_list('slug', flat=True))
        tag_obj.setdefault(tag[1], [])
        tag_obj[tag[1]].append(ex)
    telemetry = list(TelemetryData.objects.filter(exercise__in=exercises).values('author__username', 'exercise__slug')
                     .annotate(max_points=Max('points')))
    data = {}
    columns = {'Name'}
    for answer in telemetry:
        columns.add(answer['exercise__slug'])
        data.setdefault(answer['author__username'], {})
        data[answer['author__username']][answer['exercise__slug']
                                         ] = round(answer['max_points'], 1)
    prepared_data = []
    exercises = list(Exercise.objects.all().values_list('slug', flat=True))
    for student in data:
        data[student].update({'Name': student})
        prepared_data.append(data[student])

    return render(request, 'dashboard/instructor-progress.html',
                  {
                      'data': prepared_data,
                      'columns': list(columns),
                      'tags': tag_obj,
                  })
