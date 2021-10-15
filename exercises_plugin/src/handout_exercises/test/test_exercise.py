from bs4 import BeautifulSoup
from collections import namedtuple

from ..exercise import CODE_TYPE, HANDOUT_GROUP, QUIZ_TYPE, TEXT_TYPE, find_code_exercises, find_exercises_in_handout
from .html_utils import admonition, admonition_title, div, el, form, p, task_list, text_question


class MockFile:
    def __init__(self, url):
        self.src_path = url
        self.url = url


def exercise_files(url):
    return [
        MockFile(f'{url}/{name}')
        for name in [
            'index.md',
            '__init__.py',
            'meta.yml',
            'solution.py',
            'test_solution.py',
            'wrong.py',
        ]
    ]


def assert_exercise(exercise, slug, url, tp, topic, group):
    assert exercise.slug == slug
    assert exercise.url == url
    assert exercise.tp == tp
    assert exercise.topic == topic
    assert exercise.group == group


def test_find_code_exercises():
    files = (
        exercise_files('handouts/recursion/exercises/fibonacci') +
        exercise_files('handouts/recursion/exercises/hanoi') +
        [MockFile('handouts/recursion/index.md')] +
        exercise_files('handouts/memoization/exercises/fibonacci') +
        [MockFile('handouts/memoization/index.md')]
    )
    expected = [
        ('handouts-recursion-exercises-fibonacci', 'handouts/recursion/exercises/fibonacci', 'recursion'),
        ('handouts-recursion-exercises-hanoi', 'handouts/recursion/exercises/hanoi', 'recursion'),
        ('handouts-memoization-exercises-fibonacci', 'handouts/memoization/exercises/fibonacci', 'memoization'),
    ]

    exercises = find_code_exercises(files)

    assert len(exercises) == len(expected)
    for exercise, (slug, url, topic) in zip(exercises, expected):
        assert_exercise(exercise, slug, url, CODE_TYPE, topic, HANDOUT_GROUP)


def test_find_exercises_in_handout():
    page_url = 'handouts/intro/'
    html = el('html', [
        el('body', [
            admonition('question choice', [
                admonition_title('Question 1'),
                p('Multiple choice'),
                form([task_list(['a', 'b', 'c', 'd'], 'c is always right.')])
            ]),
            div([
                text_question('Short question with id', 'What did the ocean say to the beach?', 'Nothing, it just waved.', 'short id_some_long_and_unique_id')
            ]),
            div([
                text_question('Short question', 'What is 1 + 1?', 'A sum', 'short')
            ]),
            div([div([
                text_question('Long question', 'What is 12345 + 54321?', 'A longer sum', 'long')
            ])])
        ]),
    ])
    exercises, new_html = find_exercises_in_handout(html, page_url)
    expected_exercises = [
        ('handouts-intro-0', QUIZ_TYPE),
        ('handouts-intro-some_long_and_unique_id', TEXT_TYPE),
        ('handouts-intro-2', TEXT_TYPE),
        ('handouts-intro-3', TEXT_TYPE),
    ]

    soup = BeautifulSoup(new_html, 'html.parser')
    html_questions = soup.select('.admonition.question')

    assert len(html_questions) == len(expected_exercises)
    assert len(exercises) == len(expected_exercises)
    for exercise, html_question, (slug, tp) in zip(exercises, html_questions, expected_exercises):
        assert_exercise(exercise, slug, page_url, tp, 'intro', HANDOUT_GROUP)
        assert html_question.attrs['id'] == slug

