from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.http import urlencode
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from core.models import Course, ExerciseTag, Exercise, TelemetryData
from core.serializers import TelemetryDataSerializer, UserSerializer
from core.shortcuts import redirect


def login_request(request):
    next_url = request.GET.get("next", None)
    if not next_url:
        next_url = request.session.get("next", None)

    request.session['next'] = next_url

    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        return redirect(next_url + '?' + urlencode({"token": token.key}))
    else:
        request.session["next"] = next_url
        return redirect("account_login")


def logout_request(request):
    next_url = request.GET.get("next", '/api/login')
    if request.user.is_authenticated:
        logout(request)
    return redirect(next_url + '?token=')


def user_menu(request):
    login_url = request.build_absolute_uri('/api/login')
    logout_url = request.build_absolute_uri('/api/logout')
    next_param = request.headers.get('Hx-Current-Url', '')
    if next_param:
        if '?token=' in next_param:
            pos = next_param.find('?token')
            next_param = next_param[:pos]
        login_url += '?' + urlencode({'next': next_param})
        logout_url += '?' + urlencode({'next': next_param})

    return render(request, "user_menu.html", {'login_url': login_url, 'logout_url': logout_url})


@api_view(['GET'])
@login_required
def user_info(request):
    user = request.user
    return Response(UserSerializer(user).data)


@api_view(['POST'])
@login_required
def telemetry_data(request):
    user = request.user
    exercise_data = request.data['exercise']
    course_name = exercise_data['course']
    slug = exercise_data['slug']
    tags = exercise_data['tags']
    points = request.data.get('points', 1)
    log = request.data['log']

    course, _ = Course.objects.get_or_create(name=course_name)
    exercise, _ = Exercise.objects.get_or_create(course=course, slug=slug)
    ensure_tags_equal(exercise, tags)
    telemetry_data = TelemetryData.objects.create(
        author=user, exercise=exercise, points=points, log=log)

    return Response(TelemetryDataSerializer(telemetry_data).data)


def ensure_tags_equal(exercise, tags):
    tags = set(tags)

    # Remove tags that no longer belong to the exercise
    for tag in exercise.tags.all():
        if tag.name in tags:
            tags.remove(tag.name)
        else:
            exercise.tags.remove(tag)

    # Add new tags
    for tag_name in tags:
        tag, _ = ExerciseTag.objects.get_or_create(
            course=exercise.course, name=tag_name)
        exercise.tags.add(tag)


@api_view(["GET"])
@permission_classes([IsAdminUser])
@login_required
def get_all_answers(request, course_name, exercise_slug):
    course = get_object_or_404(Course, name=course_name)
    exercise = get_object_or_404(Exercise, course=course, slug=exercise_slug)
    data = TelemetryData.objects.filter(exercise=exercise, last=True)
    return Response(TelemetryDataSerializer(data, many=True).data)
