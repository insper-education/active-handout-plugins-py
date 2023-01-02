from urllib.parse import unquote
import json

from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from core.models import Course, User
from dashboard.query import StudentStats


@xframe_options_exempt
@login_required
def student_dashboard(request, course_name, student_id):
    student = get_object_or_404(User, pk=student_id)
    if request.user != student and not request.user.is_staff:
        raise PermissionDenied("Can't get dashboard for another user, except if user is admin")

    course_name = unquote(course_name)
    course = get_object_or_404(Course, name=course_name)

    tag_tree = json.loads(request.GET.get('tag-tree', '{}'))

    student_stats = StudentStats(student, course, tag_tree)

    return render(request, 'dashboard/student-dashboard.html', {
        'referer': request.META.get('HTTP_REFERER', ''),
        'course': course,
        'tags': student_stats.tags,
        'tag_tree': tag_tree,
        'tag_stats': student_stats.stats_by_tag_group,
        'total_exercises': student_stats.total_exercises,
        'exercise_count_by_tag_slug_and_date': student_stats.exercise_count_by_tag_slug_and_date,
    })
