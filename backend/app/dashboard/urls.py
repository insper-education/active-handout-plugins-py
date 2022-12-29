from django.urls import path
from dashboard import views


urlpatterns = [
    path("fragments/student/<int:student_id>", views.student_dashboard_fragment, name='student-dashboard-fragment'),
]
