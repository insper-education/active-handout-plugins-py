from bs4 import BeautifulSoup
from pymdownx.slugs import slugify
import requests
import re
from pathlib import Path
from urllib.parse import quote_plus
import yaml


HANDOUT_GROUP = 'handout'
CODE_TYPE = 'CODE'
QUIZ_TYPE = 'QUIZ'
TEXT_TYPE = 'TEXT'

EXERCISE_LIST_REGEX = r'^\s*!!!\s*exercise-list\s*'

class Exercise:
    def __init__(self, slug, url, tp, topic, group):
        self.slug = slug
        self.url = url
        self.tp = tp
        self.topic = topic
        self.group = group

    def __str__(self):
        return self.slug

    def to_dict(self):
        return {
            'slug': self.slug,
            'url': self.url,
            'type': self.tp,
            'topic': self.topic,
            'group': self.group,
        }


class CodeExercise(Exercise):
    def __init__(self, meta_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_file = meta_file
        try:
            with open(self.meta_file.abs_src_path) as f:
                self.meta = yaml.safe_load(f)
            self._init_title()
        except FileNotFoundError:
            self.meta = None

    def _init_title(self):
        try:
            with open(Path(self.meta_file.abs_src_path).parent / 'index.md') as f:
                self.meta['title'] = get_title(f.read())
        except FileNotFoundError:
            return


def extract_topic(url):
    split_url = url.split('/')
    if len(split_url) < 2:
        return url
    return split_url[1]


def find_code_exercises(files):
    exercises = []

    for f in files:
        if f.src_path.endswith('meta.yml'):
            slug_url = f.url[:-len('meta.yml')]
            slug_url = slug_url.replace('/', ' ').strip()
            exercise_url = str(Path(f.url).parent)
            topic = extract_topic(f.url)
            exercises.append(CodeExercise(f, slugify()(slug_url, '-'), exercise_url, CODE_TYPE, topic, HANDOUT_GROUP))

    return exercises


def find_exercises_in_handout(html, page_url):
    exercises = []

    soup = BeautifulSoup(html, 'html.parser')
    page_slug = page_url.replace('/', '-')
    for idx, ex in enumerate(soup.select('.admonition.question')):
        slug = str(idx)
        for c in ex['class']:
            if c.startswith('id_'):
                slug = c[3:]
                break

        tp = QUIZ_TYPE
        if 'css-exercise' in ex['class']:
            tp = 'CSS'
        elif 'short' in ex['class'] or 'long' in ex['class']:
            tp = TEXT_TYPE

        ex['id'] = slug = page_slug + slug
        topic = extract_topic(page_url)
        exercises.append(Exercise(slug, page_url, tp, topic, HANDOUT_GROUP))

    new_html = str(soup)
    return exercises, new_html


def post_exercises(exercises, token, report_url):
    for exercise in exercises:
        try:
            st = requests.post(report_url, data=exercise.to_dict(), headers={
                'Authorization': f'Token {token}'
            })
        except Exception:
            print("Couldn't post exercise", exercise)


def get_meta_for(page_file, files):
    if not page_file.src_path.endswith('index.md'):
        return None

    meta_filename = str(Path(page_file.src_path).parent / 'meta.yml')
    for file in files:
        if file.src_path == meta_filename:
            return file
    return None


def has_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return True
    return False


def get_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[1:].strip()
    return None


def is_exercise_list(markdown):
    for line in markdown.split('\n'):
        if re.search(EXERCISE_LIST_REGEX, line):
            return True
    return False


def add_vscode_button(markdown, meta_file, base_url):
    ext_url = 'vscode://insper.devlife/'
    exercise_addr = quote_plus(f'{base_url}{meta_file.url}')
    full_url = f'{ext_url}?exercise_addr={exercise_addr}'

    button_text = 'Resolver exercício'
    icon = ':material-microsoft-visual-studio-code:'
    extra_classes = '{ .md-button .md-button--primary }'
    vscode_button = f'[{button_text} {icon}]({full_url}){extra_classes}'

    return f'{markdown}\n\n{vscode_button}\n'


def override_yaml(abs_dest_path, overrides):
    with open(abs_dest_path) as f:
        data = yaml.safe_load(f)
    data.update(overrides)
    with open(abs_dest_path, 'w') as f:
        yaml.safe_dump(data, f, encoding='utf-8', allow_unicode=True)


def sorted_exercise_list(src_path, code_exercises_by_path):
    base_path = str(Path(src_path).parent)
    exercises = []

    for path, exercise in code_exercises_by_path.items():
        if base_path in path:
            exercises.append(exercise)

    return sorted(exercises, key=lambda e: (e.meta['difficulty'], -e.meta['weight']))


def replace_exercise_list(markdown, exercises, base_url):
    exercises_md = '\n'.join(
        [
            f'- [[Nível {e.meta["difficulty"]}] {e.meta["title"]}]({base_url}{Path(e.url)})'
            for e in exercises
        ]
    )
    return '\n'.join(
        re.sub(EXERCISE_LIST_REGEX, exercises_md, line)
        for line in markdown.split('\n')
    )
