from django.urls import path
from dashboard import views


urlpatterns = [
    path("<str:course_name>/student", views.student_dashboard, name='student-dashboard'),
    path("<str:course_name>/heatmap", views.exercise_heatmap, name='exercise_heatmap'),
]
