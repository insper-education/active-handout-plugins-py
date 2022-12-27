from django.urls import path
from core import views


urlpatterns = [
    path("telemetry", views.telemetry_data, name='telemetry-data'),
    path("login", views.login_request, name='view-login'),
    path("logout", views.logout_request, name='view-logout'),
    path("user-info", views.user_info, name='user-info'),
    path("user-menu", views.user_menu, name='user-menu'),
]
