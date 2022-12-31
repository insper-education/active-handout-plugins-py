from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student/<int:student_id>", views.student_dashboard, name='student-dashboard'),
]
