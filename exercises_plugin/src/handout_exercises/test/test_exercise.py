from bs4 import BeautifulSoup
import yaml

from ..exercise import CODE_TYPE, HANDOUT_GROUP, QUIZ_TYPE, TEXT_TYPE, CodeExercise, Exercise, add_vscode_button, extract_topic, find_code_exercises, find_exercises_in_handout, get_title, is_exercise_list, replace_exercise_list, sorted_exercise_list
from .html_utils import admonition, admonition_title, div, el, form, p, task_list, text_question


BASE_URL = 'http://localhost:8000/goat-cheese/'

class MockFile:
    def __init__(self, url):
        self.src_path = url
        self.abs_src_path = url
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
            'exemplo.py',
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

    exercises = find_code_exercises(files, 1)

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


def test_get_title():
    assert get_title('''# Title here

    Some text here
''') == 'Title here'
    assert get_title('''
# This is a title

    Some text here
''') == 'This is a title'
    assert get_title('''
    # This is a comment in a code block

    Some text here
''') == None
    assert get_title('''
    Just some text

    Some additional text here
''') == None


def test_is_exercise_list():
    for prev_lines in range(3):
        for after_lines in range(3):
            for init_spaces in range(4):
                for mid_spaces in range(4):
                    for end_spaces in range(4):
                        markdown = (
                            prev_lines * '\n' +
                            init_spaces * ' ' +
                            '!!!' +
                            mid_spaces * ' ' +
                            'exercise-list' +
                            end_spaces * ' ' +
                            after_lines * '\n'
                        )
                        assert is_exercise_list(markdown) == True
    assert is_exercise_list('!!! not-exercise-list') == False

def test_add_vscode_button():
    original_md = '''
# Exercise title

Exercise statement
in multiple lines
'''
    meta_file = MockFile('handouts/recursion/exercises/fibonacci/meta.yml')
    output_md = add_vscode_button(original_md, meta_file, BASE_URL)
    assert output_md == '''
# Exercise title

Exercise statement
in multiple lines


[Resolver exercício :material-microsoft-visual-studio-code:](vscode://insper-comp.devlife/?exercise_addr=http%3A%2F%2Flocalhost%3A8000%2Fgoat-cheese%2Fhandouts%2Frecursion%2Fexercises%2Ffibonacci%2Fmeta.yml){ .md-button .md-button--primary }
'''


def add_exercise_to_path(url, slug, group, meta, code_exercises_by_path):
    exercise = Exercise(slug, url, CODE_TYPE, group)
    exercise.meta_file = MockFile(url)
    exercise.meta = meta
    code_exercises_by_path[url] = exercise
    return exercise


def make_meta(title, difficulty, weight, slug):
    return {
        'title': title,
        'difficulty': difficulty,
        'weight': weight,
        'slug': slug,
        'offering': 1,
        'testFile': 'test_solution.py',
        'studentFile': 'solution.py',

    }


def test_sorted_exercise_list():
    code_exercises_by_path = {}
    add_exercise_to_path(
        'handouts/recursion/exercises/fibonacci',
        'recursion-fibonacci',
        HANDOUT_GROUP,
        make_meta('Fibonacci', 2, 2, 'recursion-fibonacci'),
        code_exercises_by_path
    )
    add_exercise_to_path(
        'handouts/recursion/exercises/sum',
        'recursion-sum',
        HANDOUT_GROUP,
        make_meta('Sum', 2, 1, 'recursion-sum'),
        code_exercises_by_path
    )
    add_exercise_to_path(
        'handouts/recursion/exercises/hanoi',
        'recursion-hanoi',
        HANDOUT_GROUP,
        make_meta('Hanoi', 4, 2, 'recursion-hanoi'),
        code_exercises_by_path
    )
    add_exercise_to_path(
        'handouts/recursion/exercises/max_diff',
        'recursion-max_diff',
        HANDOUT_GROUP,
        make_meta('Maximum difference', 4, 3, 'max_diff'),
        code_exercises_by_path
    )
    add_exercise_to_path(
        'handouts/memoization/exercises/fibonacci',
        'memoization-fibonacci',
        HANDOUT_GROUP,
        make_meta('Fibonacci', 2, 1, 'memoization-fibonacci'),
        code_exercises_by_path
    )
    output = sorted_exercise_list(
        'handouts/recursion/exercises/index.md',
        code_exercises_by_path
    )
    expected = [
        code_exercises_by_path[f'handouts/recursion/exercises/{slug}']
        for slug in ['fibonacci', 'sum', 'max_diff', 'hanoi']
    ]
    assert expected == output


def test_replace_exercise_list():
    code_exercises_by_path = {}
    exercises = [
        add_exercise_to_path(
            'handouts/recursion/exercises/fibonacci',
            'recursion-fibonacci',
            HANDOUT_GROUP,
            make_meta('Fibonacci', 2, 2, 'recursion-fibonacci'),
            code_exercises_by_path
        ),
        add_exercise_to_path(
            'handouts/recursion/exercises/sum',
            'recursion-sum',
            HANDOUT_GROUP,
            make_meta('Sum', 3, 1, 'recursion-sum'),
            code_exercises_by_path
        )
    ]

    expected = f'''
- [[Nível 2] Fibonacci]({BASE_URL}handouts/recursion/exercises/fibonacci)
- [[Nível 3] Sum]({BASE_URL}handouts/recursion/exercises/sum)
'''.strip()
    assert expected in replace_exercise_list('!!! exercise-list', exercises, BASE_URL)
    assert expected in replace_exercise_list('# Title\n\n!!! exercise-list\n\n', exercises, BASE_URL)


def test_extract_topic():
    urls = (
        ('aulas/fatiamento/exercises/capitaliza_string/meta.yml', 'fatiamento'),
        ('aulas/for/exercises/valor_da_nota_fiscal/meta.yml', 'for'),
        ('aulas/if/exercises/exercises/todo_mundo_odeia_o_chris/meta.yml', 'if'),
        ('aulas/if/exercises/exercises/calculo_de_aumento_de_salario/meta.yml', 'if'),
        ('aulas/lista/exercises/soma_dos_numero_impares/meta.yml', 'lista'),
        ('aulas/lista/exercises/soma_valores_da_lista/meta.yml', 'lista'),
        ('aulas/string/exercises/esconde_senha/meta.yml', 'string'),
        ('aulas/while/exercises/aluno_com_duvidas/meta.yml', 'while'),
        ('aulas/while/exercises/quantos_uns/meta.yml', 'while'),
        ('aulas/while/exercises/raiz_quadrada_por_subtracoes/meta.yml', 'while'),
    )
    for url, expected in urls:
        topic = extract_topic(url)
        assert topic == expected


def create_file(filename, content):
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)


def create_exercise_in_path(root):
    root.mkdir(parents=True)

    meta = {
        'difficulty': 2,
        'weight': 1,
        'offering': 1,
        'testFile': 'test_solution.py',
        'studentFile': 'solution.py',
    }
    meta_filename = root / 'meta.yml'
    with open(meta_filename, 'w') as f:
        yaml.safe_dump(meta, f, encoding='utf-8', allow_unicode=True)
    create_file(root / 'index.md', '# Hanoi\n\nSolve hanoi recursivelly.')
    create_file(root / 'solution.py', 'print("Oh no...")')
    create_file(root / '__pycache__' / 'solution.pyc', '')
    create_file(root / 'test_solution.py', 'def test_pass():\n    assert True')
    create_file(root / 'submodule' / 'functions.py', '# Some functions here')
    create_file(root / 'submodule' / '__pycache__' / 'functions.pyc', '')


def test_ignore_files_in_meta(tmp_path):
    root = tmp_path / 'devlife-content/content/topics/recursion/exercises/hanoi'
    create_exercise_in_path(root)

    slug = 'recursion-max_diff'
    url = 'handouts/recursion/exercises/max_diff'
    tp = CODE_TYPE
    group = HANDOUT_GROUP
    exercise = CodeExercise(MockFile(root / 'meta.yml'), 1, slug, url, tp, group)

    expected_files = ['index.md', 'solution.py', 'test_solution.py', 'submodule/functions.py']
    assert len(exercise.meta['files']) == len(expected_files)
    for f in expected_files:
        assert f in exercise.meta['files']


def test_auto_add_offering_to_meta(tmp_path):
    root = tmp_path / 'devlife-content/content/topics/recursion/exercises/hanoi'
    create_exercise_in_path(root)

    slug = 'recursion-max_diff'
    url = 'handouts/recursion/exercises/max_diff'
    tp = CODE_TYPE
    group = HANDOUT_GROUP
    offering_id = 10
    exercise = CodeExercise(MockFile(root / 'meta.yml'), offering_id, slug, url, tp, group)

    assert exercise.meta['offering'] == offering_id
