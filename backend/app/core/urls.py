from django.urls import path, re_path
from core import views


urlpatterns = [
    # Telemetry Data related
    path("telemetry", views.telemetry_data, name='telemetry-data'),
    re_path("telemetry/answers/", views.get_all_answers),

    # Auth related
    path("login", views.login_request, name='view-login'),
    path("logout", views.logout_request, name='view-logout'),
    path("user-info", views.user_info, name='user-info'),
    path("user-menu", views.user_menu, name='user-menu'),
    path("user-token", views.user_token, name='user-token'),

    # Update/Retrieve exercise data
    path("exercises/<str:course_name>", views.exercise_list),
    path("exercises/<str:course_name>/<str:exercise_slug>/enable", views.enable_exercise),
    path("exercises/<str:course_name>/<str:exercise_slug>/disable", views.disable_exercise),

    # Tag data
    path("tags/<str:course_name>/names", views.update_tag_names),
]
