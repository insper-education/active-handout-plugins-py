from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied

from core.models import User


@login_required
def student_dashboard_fragment(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    if request.user != student and not request.user.is_staff:
        raise PermissionDenied("Can't get dashboard for another user, except if user is admin")

    return render('dashboard/fragments/student-dashboard.html')
