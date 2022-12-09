from core.models import Enrollment, Offering
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

class IsAdminOrSelf(IsAdminUser):
    """
    Allow access to admin users or the users themselves.
    """
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_staff:
                return True
            elif type(obj) == type(request.user) and obj == request.user:
                return True
        return False


class IsEnrolledInOfferingOrIsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user:
            return False

        if request.user.is_staff:
            return True

        offering_pk = view.kwargs.get('off_pk')
        try:
            offering = Enrollment.objects.get(student=request.user.pk, offering=offering_pk)
            return True
        except Enrollment.DoesNotExist:
            return False
