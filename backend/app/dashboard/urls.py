from django.urls import path
from core import views


urlpatterns = [
    path("fragments/student/<int:student_id>", views.student_dashboard_fragment, name='student-dashboard-fragment'),
]
