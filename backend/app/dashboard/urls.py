from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("instructor", views.instructor_courses, name='instructor-courses'),
    path("instructor/<str:course_name>", views.instructor_dashboard, name='instructor-dashboard'),
    path("instructor/<str:course_name>/<path:exercise_slug>", views.get_exercise_data),

]
