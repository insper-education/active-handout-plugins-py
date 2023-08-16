from urllib.parse import unquote_plus
import json

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from core.models import Course, Exercise, TelemetryData, ExerciseTag, Student, User
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

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    students = Student.objects.all()
    """telemetry = list(TelemetryData.objects.filter(exercise__in=exercises)
                     .values('author__username')
                     .annotate(total=Count('author'))
                     .order_by("total"))
    print(telemetry[:100])"""

    # a = TelemetryData.objects.raw("SELECT author, points FROM core_telemetrydata ")

    return render(request, 'dashboard/instructor-progress-weekly.html', {"students": list(students)})


@staff_member_required
@api_view()
@login_required
def student_weekly_progress(request, course_name, user_nickname, week):
    from django.db.models import Count
    from datetime import datetime, timedelta, date

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    student = get_object_or_404(Student, username=user_nickname)

    def get_past_sunday_date(weeks_ago):
        current_date = datetime.now()
        # Monday is 0, Tuesday is 1, ..., Sunday is 6
        current_day = current_date.weekday()

        days_until_last_sunday = current_day + 1 if current_day != 6 else 0

        days_ago = weeks_ago * 7 + days_until_last_sunday

        return current_date - timedelta(days=days_ago)

    week_start = get_past_sunday_date(week)
    week_end = get_past_sunday_date(week-1)

    exercises = TelemetryData.objects.filter(
        exercise__in=exercises, author=student,
        submission_date__gte=week_start, submission_date__lte=week_end
    ).values(
        "exercise__slug", "points", "exercise__tags__name"
    )

    exercise_data = {}
    for exercise in exercises:
        exercise_slug = exercise["exercise__slug"]
        if exercise_slug not in exercise_data:
            exercise_data[exercise_slug] = {
                "slug": exercise_slug,
                "points": exercise["points"],
                "tags": [exercise["exercise__tags__name"]] if exercise["exercise__tags__name"] else [],
            }
        else:
            if exercise["exercise__tags__name"]:
                exercise_data[exercise_slug]["tags"].append(
                    exercise["exercise__tags__name"])

    metrics = {}
    metrics["total"] = len(exercise_data)
    metrics["exercises"] = []
    metrics["tags"] = {}
    aggr_points = 0
    for ex in exercise_data.keys():
        aggr_points += exercise_data[ex]["points"]
        metrics["exercises"].append(
            (exercise_data[ex]["slug"], exercise_data[ex]["points"]))
        for tag in exercise_data[ex]["tags"]:
            metrics["tags"].setdefault(tag, 0)
            metrics["tags"][tag] += 1
    metrics["average_points"] = aggr_points / \
        metrics["total"] if metrics["total"] != 0 else 0
    return Response(metrics)
