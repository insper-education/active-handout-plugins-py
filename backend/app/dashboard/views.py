from urllib.parse import unquote
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from core.models import Course, User
from dashboard.query import get_stats_by_tag_group


@login_required
def student_dashboard_fragment(request, course_name, student_id):
    student = get_object_or_404(User, pk=student_id)
    if request.user != student and not request.user.is_staff:
        raise PermissionDenied("Can't get dashboard for another user, except if user is admin")

    course_name = unquote(course_name)
    course = get_object_or_404(Course, name=course_name)

    tag_tree = json.loads(request.GET.get('tag-tree', '{}'))

    tag_stats = get_stats_by_tag_group(tag_tree, course, student)

    return render(request, 'dashboard/fragments/student-dashboard.html', {
        'tag_tree': tag_tree,
        'tag_stats': tag_stats,
    })
