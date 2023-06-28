from urllib.parse import unquote_plus
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from core.models import Course, Exercise, TelemetryData
from dashboard.query import StudentStats


@api_view()
@login_required
def student_dashboard(request, course_name):
    student = request.user

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)

    tag_tree_yaml = json.loads(request.GET.get('tag-tree', '{}'))

    student_stats = StudentStats(student, course, tag_tree_yaml)

    return render(request, 'dashboard/student-dashboard.html', {
        'referer': request.META.get('HTTP_REFERER', ''),
        'course': course,
        'tags': student_stats.tags,
        'tag_tree': student_stats.tag_tree,
        'tag_stats': student_stats.stats_by_tag_group,
        'total_exercises': student_stats.total_exercises,
        'exercise_count_by_tag_slug_and_date': student_stats.exercise_count_by_tag_slug_and_date,
    })

@api_view()
@login_required
def instructor_courses(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/instructor-courses.html',{"courses" : courses})

@api_view()
@login_required
def instructor_dashboard(request, course_name):
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    exercise_data = []
    for ex in exercises:
        tags = [tag.name for tag in ex.tags.all() if tag.name != None]
        data = {"exercise": ex, "tags": tags}
        exercise_data.append(data)
    
    return render(request, 'dashboard/instructor-dashboard.html',{"exercise_data" : exercise_data})

@api_view()
@login_required
def get_exercise_data(request, course_name, exercise_slug):

    def convert_to_valid_json(data):
        data = data.replace("'", '"').replace('"', r'\"')
        return data

    course = get_object_or_404(Course, name=course_name)
    exercise = get_object_or_404(Exercise, course=course, slug=exercise_slug)
    
    answers = {}
    telemetry = list(TelemetryData.objects.filter(exercise=exercise, last=True).values_list('log', flat=True))
    correct = ""
    tags = [tag.name for tag in exercise.tags.all() if tag.name != None]

    if 'choice-exercise'in tags:
        answers = {x:telemetry.count(x) for x in telemetry}
        tag = 'choice'
    elif 'parsons-exercise'in tags:
        # count number of times that each code key value inside telemetry ocurred
        answers = {convert_to_valid_json(x['code'].replace('\n', '\\n')): telemetry.count(x) for x in telemetry if x['code']}
        correct = convert_to_valid_json(next((x['code'].replace('\n', '\\n') for x in telemetry if (x['correct'] and x['code'])), ''))
        tag = 'parsons'
    elif 'text-exercise'in tags:
        import re
        import nltk
        from nltk.corpus import stopwords

        nltk.download('stopwords')
        words = {}
        text = " ".join(telemetry)
        text_data = re.sub('[^a-zA-Z]', ' ', text)
        text_data = text_data.lower()
        #TODO  WordNetLemmatizer Em português
        for word in text_data.split():
            if word not in stopwords.words():
                words[word] = 1 + words.setdefault(word, 0)

        answers = [[k,str(10*v)] for k,v in words.items()]
        tag = 'text'
        
    return render(request, 'dashboard/exercise-component.html', {"answers":answers, "correct": correct, "tag": tag, 'slug': exercise_slug})
