from urllib.parse import unquote_plus
import json
import math
from datetime import datetime, timedelta


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from core.models import Course, CourseClass, Exercise, TelemetryData, Student
from dashboard.query import StudentStats
from django.db.models import Max, Count, Q


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
def instructor_courses(request, course_name=None, content_type=None):
    if course_name == None:
        course_name = Course.objects.first().name
    if content_type == 'weekly':
        return weekly_progress(request, course_name)
    return students_progress(request, course_name)


def students_progress(request, course_name):

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    course_classes = course.courseclass_set.all().prefetch_related('students')
    course_classes_list = [
        {'name': course_class.name, 'students': list(
            course_class.students.values_list('username', flat=True))}
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
                        'Name': answer['author__username']})
        data[answer['author__username']][answer['exercise__slug']
                                         ] = round(answer['max_points'], 1)
    sorted_columns = sorted(list(columns))
    columns_with_list = [*['Name'], *sorted_columns]

    data_list = sorted(list(data.values()), key=lambda d: d['Name'].lower())
    courses = Course.objects.all()

    return render(request, 'dashboard/instructor-progress.html',
                  {
                      'data': data_list,
                      'columns': columns_with_list,
                      'tags': tag_obj,
                      'course_classes': course_classes_list,
                      'courses': courses,
                      'activeCourse': course_name

                  })


def weekly_progress(request, course_name):
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    course_classes = course.courseclass_set.all().prefetch_related('students')
    course_classes_list = [
        {'name': course_class.name, 'students': list(
            course_class.students.values_list('username', flat=True))}
        for course_class in course_classes
    ]
    students = Student.objects.all()

    def generate_weeks(start_date, end_date):
        week_obj = {}

        current_date = start_date
        week_number = 1
        current_month = None
        if current_date.weekday() != 6:  # set to sunday if it is not
            current_date = current_date - \
                timedelta(days=current_date.weekday() + 1)
        while current_date <= end_date:
            end_week = current_date + timedelta(days=6)
            if current_month != current_date.month:  # reset WeekX to 1
                current_month = current_date.month
                week_number = 1
            # if last week from a month ends in the next one, reset WeekX to 1
            if current_date.month != end_week.month:
                week_number = 1
                current_month = end_week.month
                week_label = f'Week{week_number}-{end_week.strftime("%b")}'
            else:
                week_label = f'Week{week_number}-{current_date.strftime("%b")}'

            week_obj[week_label] = current_date.isoformat()
            week_number += 1
            current_date += timedelta(days=7)

        return week_obj

    start_date = course.start_date
    end_date = course.end_date

    if (start_date or end_date):
        week_obj = generate_weeks(start_date, end_date)
    else:
        week_obj = None
    courses = Course.objects.all()

    return render(request, 'dashboard/instructor-progress-weekly.html',
                  {
                      'students': list(students),
                      'weeks': week_obj,
                      'courses': courses,
                      'course_classes': course_classes_list,
                      'activeCourse': course_name
                  })


@staff_member_required
@api_view()
@login_required
def student_weekly_data(request, course_name, class_name, user_nickname, week):
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    student = get_object_or_404(Student, username=user_nickname)

    week_start = datetime.fromisoformat(week)
    week_end = week_start + timedelta(days=6)

    exercises = TelemetryData.objects.filter(
        exercise__in=exercises, author=student,
        submission_date__gte=week_start, submission_date__lte=week_end
    ).prefetch_related('exercise__tags')

    metrics = {
        'total': len(exercises),
        'exercises': {},
        'tags': {},
    }
    aggr_points = 0
    for exercise in exercises:
        exercise_slug = exercise.exercise.slug
        exercise_points = round(exercise.points, 2)
        exercise_tags = list(
            exercise.exercise.tags.all().values_list('name', flat=True))
        aggr_points += exercise_points
        if exercise_slug not in metrics['exercises']:
            metrics['exercises'][exercise_slug] = {
                'slug': exercise_slug,
                'best_score': exercise_points,
                'submissions': 1,
            }
            for tag in exercise_tags:
                metrics['tags'].setdefault(tag, 0)
                metrics['tags'][tag] += 1
        else:
            metrics['exercises'][exercise_slug]['submissions'] += 1
            if exercise_points > metrics['exercises'][exercise_slug]['best_score']:
                metrics['exercises'][exercise_slug]['best_score'] = exercise_points

    metrics['average_points'] = aggr_points / \
        metrics['total'] if metrics['total'] != 0 else 0

    return Response(metrics)


@staff_member_required
@api_view()
@login_required
def weekly_exercises(request, course_name, class_name, week):

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    class_name = unquote_plus(class_name)
    course_class = get_object_or_404(CourseClass, name=class_name)
    exercises = Exercise.objects.filter(course=course)

    week_start = datetime.fromisoformat(week)
    week_end = week_start + timedelta(days=6)

    user_exercise_counts = Student.objects.filter(courseclass=course_class).annotate(
        exercise_count=Count('telemetrydata',
                             filter=Q(telemetrydata__submission_date__gte=week_start,
                                      telemetrydata__submission_date__lte=week_end, telemetrydata__exercise__in=exercises))
    ).values('username', 'exercise_count')
    hist = {}
    granularity = 5
    # converting to histogram
    for user in user_exercise_counts:
        exercise_count = int(
            math.ceil(user['exercise_count'] / granularity)) * granularity
        if exercise_count >= 50:
            exercise_count = '>50'
        hist.setdefault(exercise_count, 0)
        hist[exercise_count] += 1

    return Response(hist)
