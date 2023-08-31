from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("instructor", views.instructor_courses, name='instructor-courses'),
    path("instructor/progress/<str:course_name>", views.students_progress),
    path("instructor/<str:course_name>/<str:content_type>", views.instructor_courses),
    path("instructor/<str:course_name>/weekly/<str:user_nickname>/<str:week>", views.student_weekly_data),
    path("instructor/<str:course_name>/weekly/<str:week>", views.weekly_exercises)

]
