from django.urls import path
from dashboard import views


urlpatterns = [
    path("fragments/<str:course_name>/student/<int:student_id>", views.student_dashboard_fragment, name='student-dashboard-fragment'),
]
