from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("instructor", views.instructor_courses, name='instructor-courses'),
    path("instructor/progress/<str:course_name>", views.students_progress),

]
