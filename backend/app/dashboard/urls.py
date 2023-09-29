from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("instructor", views.instructor_courses, name='instructor-dashboard'),
    path("instructor/<str:course_name>", views.instructor_courses, name='instructor-dashboard'),
    path("instructor/<str:content_type>/<str:course_name>", views.instructor_courses, name='instructor-dashboard'),
    path("instructor/weekly/<str:class_name>/<str:user_nickname>/<str:week>", views.student_weekly_data),
    path("instructor/weekly/<str:course_name>/<str:class_name>/<str:week>", views.weekly_exercises),
    path("instructor/student/<str:course_name>/<str:user_nickname>/", views.student_telemetry_data),


]
