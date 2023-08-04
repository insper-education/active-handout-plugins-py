from urllib.parse import unquote_plus
import json
import numpy as np
import pandas as pd

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from django.contrib.admin.views.decorators import staff_member_required

from core.models import Course, TelemetryData, Exercise
from dashboard.query import StudentStats

import plotly.graph_objects as go

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
@staff_member_required
def exercise_heatmap(request, course_name):
    exercises = Exercise.objects.filter(course__name=course_name).filter(slug__startswith="aulas/python").values_list('slug', flat=True)
    exercises = list(exercises)
    
    tag_order = [
        'introducao',
        'funcao',
        'input',
        'if',
        'while',
        'algoritmos-1',
        'lista',
        'for',
        'string',
        'dicionario',
        'arquivo',
        'classes',
    ]

    exercises.sort(key=lambda e: (
        tag_order.index(e.split('/')[2]) if e.split('/')[2] in tag_order else 999,
    ))
    
    exercises = list(map(lambda e: e.split('/')[2]+"/"+e.split('/')[-1], exercises))
    
    tel_data = TelemetryData.objects \
        .filter(last = 1).filter(author__is_staff = False) \
        .filter(exercise__course__name__startswith = course_name) \
        .filter(exercise__slug__startswith = "aulas/python") \
        .prefetch_related('author', 'exercise') \
        .all()
    # .filter(submission_date__range=["2023-02-01", "2023-02-7"]) \

    dataframe = pd.DataFrame(columns=exercises)

    for data in tel_data:
        username = data.author.username
        slug = data.exercise.slug
        slug = slug.split("/")[2]+"/"+slug.split("/")[-1]
        points = data.points

        if slug not in dataframe.columns:
            dataframe[slug] = np.nan
            print(slug + " não está no dataframe")
        if username not in dataframe.index:
            dataframe.loc[username] = np.nan
        dataframe.loc[username, slug] = points
    
    dataframe = dataframe.sort_index()
    names = dataframe.index
    exercise_list = dataframe.columns
    data = dataframe.to_numpy()

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=data,
        x=exercise_list,
        y=names,
        hovertemplate = 'Exercício: %{x}<br> Aluno: %{y}<br> Nota: %{z}<extra></extra>',
        colorscale=[(0.0, "red"), (0.1, "red"),
                    (0.1, "yellow"), (0.5, "yellow"),
                    (0.5, "orange"), (1, "orange"),
                    (1, "green"),  (1.00, "green")],
        showscale=False,
        xgap=0.5,
        ygap=0.5
    ))
    fig.update_xaxes(showticklabels=False)
    fig.update_xaxes(side="top")

    fig.update_layout(
        xaxis=dict(title="Exercício"),
        yaxis=dict(title="Username", autorange="reversed"),
        autosize=True,
        height=len(names)*25,
        
    )
    
    chart = fig.to_html()

    return render(request, 'dashboard/exercise-heatmap.html', {"chart": chart})