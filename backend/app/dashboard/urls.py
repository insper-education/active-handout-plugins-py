from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("instructor", views.instructor_courses, name='instructor-courses'),
    path("instructor/progress/<str:course_name>", views.students_progress),
    path("instructor/progress/weekly/<str:course_name>", views.weekly_progress),
    path("instructor/progress/weekly/<str:course_name>/<str:user_nickname>/<str:week>", views.student_weekly_progress)

]
