from urllib.parse import unquote_plus
import json

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view


from core.models import Course, Exercise, TelemetryData, ExerciseTag, Student
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
    columns_with_list = [*["Name"], *list(columns)]
    return render(request, 'dashboard/instructor-progress.html',
                  {
                      'data': list(data.values()),
                      'columns': columns_with_list,
                      'tags': tag_obj,
                  })

@staff_member_required
@api_view()
@login_required
def weekly_progress(request, course_name):
    from django.db.models import Count
    import datetime

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    students = Student.objects.all()
    """telemetry = list(TelemetryData.objects.filter(exercise__in=exercises)
                     .values('author__username')
                     .annotate(total=Count('author'))
                     .order_by("total"))
    print(telemetry[:100])"""

    #a = TelemetryData.objects.raw("SELECT author, points FROM core_telemetrydata ")
    a = (TelemetryData.objects.filter(exercise__in=exercises)
         .values('author__username')
         .annotate(total=Count('author'))
         .filter(
        submission_date__gte=datetime.date(2023, 4,1),
        submission_date__lte=datetime.date(2023,5,1)
        )
    )
    return render(request, 'dashboard/instructor-progress-weekly.html',{"students":list(students)})
