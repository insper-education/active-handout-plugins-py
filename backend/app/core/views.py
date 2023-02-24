from urllib.parse import unquote_plus
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.http import urlencode
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from core.models import Course, ExerciseTag, Exercise, TelemetryData, User
from core.serializers import TelemetryDataSerializer, UserSerializer
from core.shortcuts import redirect

from urllib.parse import unquote


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


@api_view(['GET'])
@login_required
def user_token(request):
    user = request.user
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, "user/token.html", {'user': user, 'token': token})


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
    if not exercise.enabled:
        raise PermissionDenied("Disabled exercise")
    ensure_tags_equal(exercise, tags)
    telemetry_data = TelemetryData.objects.create(
        author=user, exercise=exercise, points=points, log=log)

    return Response(TelemetryDataSerializer(telemetry_data).data)


def ensure_tags_equal(exercise, tags):
    tags = set(tags)

    # Remove tags that no longer belong to the exercise
    for tag in exercise.tags.all():
        if tag.slug in tags:
            tags.remove(tag.slug)
        else:
            exercise.tags.remove(tag)

    # Add new tags
    for tag_slug in tags:
        tag, _ = ExerciseTag.objects.get_or_create(
            course=exercise.course, slug=tag_slug)
        exercise.tags.add(tag)


@api_view(["GET"])
@permission_classes([IsAdminUser])
@login_required
def get_all_answers(request):
    course_name = unquote(request.GET.get('course_name', ''))
    exercise_slug = unquote(request.GET.get('exercise_slug', ''))
    
    course = get_object_or_404(Course, name=course_name)
    exercise = get_object_or_404(Exercise, course=course, slug=exercise_slug)
    data = TelemetryData.objects.filter(exercise=exercise, last=True)
    return Response(TelemetryDataSerializer(data, many=True).data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
@login_required
def exercise_list(request, course_name):
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercise_list = request.data

    tags_by_slug = {
        exercise_data['slug']: exercise_data['tags']
        for page in exercise_list.values()
        for exercise_data in page.values()
    }
    total_created = 0
    total_updated = 0
    for slug, tags in tags_by_slug.items():
        exercise, created = Exercise.objects.get_or_create(course=course, slug=slug)
        ensure_tags_equal(exercise, tags)

        if created:
            total_created += 1
        else:
            total_updated += 1

    return Response({"created": total_created, "updated": total_updated})


@api_view(["GET"])
@permission_classes([IsAdminUser])
@login_required
def enable_exercise(request, course_name, exercise_slug):
    course = get_object_or_404(Course, name=course_name)
    exercise = get_object_or_404(Exercise, course=course, slug=exercise_slug)
    exercise.enabled = True
    exercise.save()
    return Response("OK")


@api_view(["GET"])
@permission_classes([IsAdminUser])
@login_required
def disable_exercise(request, course_name, exercise_slug):
    course = get_object_or_404(Course, name=course_name)
    exercise = get_object_or_404(Exercise, course=course, slug=exercise_slug)
    exercise.enabled = False
    exercise.save()
    return Response("OK")


@api_view(["POST"])
@permission_classes([IsAdminUser])
@login_required
def update_tag_names(request, course_name):
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    slug_to_name = request.data
    tag_slugs = slug_to_name.keys()
    tags = ExerciseTag.objects.filter(course=course, slug__in=tag_slugs)
    to_update = []
    for tag in tags:
        name = slug_to_name.get(tag.slug)
        if name:
            tag.name = name
            to_update.append(tag)
    if to_update:
        ExerciseTag.objects.bulk_update(to_update, ['name'])
    return Response({"updated": len(to_update)})
