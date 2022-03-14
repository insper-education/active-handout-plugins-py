from bs4 import BeautifulSoup
from pymdownx.slugs import slugify
import requests
import re
from pathlib import Path
from urllib.parse import quote_plus
import yaml
import json


EXTRA_GROUP = 'extra'
HANDOUT_GROUP = 'handout'
CODE_TYPE = 'CODE'
QUIZ_TYPE = 'QUIZ'
TEXT_TYPE = 'TEXT'
CSS_TYPE = 'CSS'
SELF_ASSESS_TYPE = 'SELF'

EXERCISE_LIST_REGEX = r'^\s*!!!\s*exercise-list\s*'

IGNORED_FILES = ['meta.yml', '__pycache__', '.pytest_cache', 'index.md', 'raw']


class Exercise:
    def __init__(self, slug, url, tp, group):
        self.slug = slug
        self.url = url
        self.tp = tp
        self.topic = extract_topic(url)
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
    def __init__(self, meta_file, offering, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_file = meta_file
        try:
            with open(self.meta_file.abs_src_path, encoding='utf-8') as f:
                self.meta = yaml.safe_load(f)
                self.meta['slug'] = self.slug
                self.meta['topic'] = self.topic
                self.meta['offering'] = offering
            self._init_title()
            self.authors = []
            self.__load_ignore_regex()
            self._list_all_files()
        except FileNotFoundError:
            self.meta = None


    def _init_title(self):
        try:
            with open(Path(self.meta_file.abs_src_path).parent / 'index.md', encoding='utf-8') as f:
                self.meta['title'] = get_title(f.read())
        except FileNotFoundError:
            return

    def __load_ignore_regex(self):
        current_folder = Path(self.meta_file.abs_src_path).parent
        try:
            with open(current_folder / '.ignore') as f:
                ignore_regex_parts = [
                    f'({s})' for s in f.readlines()
                ]
                self.ignore_regex = re.compile('|'.join(ignore_regex_parts))
        except IOError:
            self.ignore_regex = None

    def __ignore_file(self, relative):
        relative_parts = relative.parts
        for ign in IGNORED_FILES:
            if ign in relative_parts:
                return True

        if self.ignore_regex:
            return re.match(self.ignore_regex, str(relative))

        return False

    def _list_all_files(self):
        current_folder = Path(self.meta_file.abs_src_path).parent
        self.meta['files'] = []
        for f in current_folder.glob('./**/*'):
            current_file = Path(f)
            try:
                relative = current_file.relative_to(current_folder)

                if not current_file.is_dir() and not self.__ignore_file(relative):
                    self.meta['files'].append(str(relative))
            except ValueError:
                continue

    def save_meta(self):
        with open(self.meta_file.abs_dest_path, 'w') as f:
            yaml.safe_dump(self.meta, f, encoding='utf-8', allow_unicode=True)


def extract_topic(url):
    split_url = url.split('/')

    ignored_folders = ['content', 'aulas']
    topic_folders = [d for d in split_url if d not in ignored_folders and d]

    ex_idx = len(topic_folders)
    if 'exercises' in topic_folders:
        ex_idx = topic_folders.index('exercises')
    if ex_idx < 1:  # We need at least one folder
        return url
    topic_folders = topic_folders[:ex_idx]

    return '/'.join(topic_folders)


def find_code_exercises(files, offering):
    exercises = []

    for f in files:
        if f.src_path.endswith('meta.yml'):
            slug_url = f.url[:-len('meta.yml')]
            slug_url = slug_url.replace('/', ' ').strip()
            exercise_url = str(Path(f.url).parent)
            exercises.append(CodeExercise(f, offering, slugify()(
                slug_url, '-'), exercise_url, CODE_TYPE, EXTRA_GROUP))

    return exercises


def find_exercises_in_handout(html, page_url, abs_path, code_exercises_by_path):
    exercises = []

    soup = BeautifulSoup(html, 'html.parser')
    page_slug = page_url.replace('/', '-')
    for idx, ex in enumerate(soup.select('.admonition.exercise')):
        slug = str(idx)
        for c in ex['class']:
            if c.startswith('id_'):
                slug = c[3:]
                break

        if 'css-exercise' in ex['class']:
            tp = CSS_TYPE
        elif 'short' in ex['class'] or 'long' in ex['class']:
            tp = TEXT_TYPE
        elif 'choice' in ex['class']:
            tp = QUIZ_TYPE
        else:
            tp = SELF_ASSESS_TYPE

        # Hide admonition until React component is loaded
        ex['class'].append('hidden')

        ex['id'] = slug = page_slug + slug
        ex['data-pageslug'] = page_slug
        exercises.append(Exercise(slug, page_url, tp, HANDOUT_GROUP))

    for ex in soup.select('.admonition.progress'):
        # Hide admonition until React component is loaded
        ex['class'].append('hidden')

    for button in soup.select('.md-button'):
        href = button.attrs['href']
        if not href or href.startswith('vscode://'):
            continue
        relative_path = href.replace('index.md', '')
        base_path = Path(abs_path)
        if base_path.name == 'index.md':  # index.md is not rendered as part of the url, so it breaks the relative paths :(
            base_path = base_path.parent
        elif base_path.name.endswith('.md'):
            base_path = base_path.parent / base_path.name.replace('.md', '/')
        ex_path = str((base_path / relative_path / 'meta.yml').resolve())  # We need resolve() because we can't have relative paths in the middle
        exercise = code_exercises_by_path.get(ex_path)
        if exercise:
            exercise.group = HANDOUT_GROUP
            admonition = button.find_parent(class_='exercise')
            if admonition:
                admonition['class'].append('code-exercise')
                admonition['id'] = exercise.slug

    new_html = str(soup)
    return exercises, new_html


def post_exercises(exercises, token, report_url):
    if token == '':
        return

    for exercise in exercises:
        try:
            st = requests.post(report_url, data=exercise.to_dict(), headers={
                'Authorization': f'Token {token}'
            })
        except Exception:
            print("Couldn't post exercise", exercise)


def export_exercises_file(exercises, site_dir):
    all_exercises = [exercise.to_dict() for exercise in exercises]

    with open(Path(site_dir) / 'exercises.json', 'w') as f:
        json.dump(all_exercises, f)


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
        if line.startswith('#'):
            return True
    return False


def get_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('#'):
            return line[1:].strip()
    return None


def is_exercise_list(markdown):
    for line in markdown.split('\n'):
        if re.search(EXERCISE_LIST_REGEX, line):
            return True
    return False


def build_vscode_button(meta_file, base_url):
    ext_url = 'vscode://insper-comp.devlife/'
    exercise_addr = quote_plus(f'{base_url}{meta_file.url}')
    full_url = f'{ext_url}?exercise_addr={exercise_addr}'

    button_text = 'Resolver exercício'
    icon = ':material-microsoft-visual-studio-code:'
    extra_classes = '{ .md-button .md-button--primary }'
    return f'[{button_text} {icon}]({full_url}){extra_classes}'


def build_submission_list_admonition(exercise):
    return f'!!! submission-list hidden slug_{exercise.slug}\n    Submission list'


def enhance_exercise_md(exercise, markdown, meta_file, base_url):
    vscode_button = build_vscode_button(meta_file, base_url)
    submission_list_admonition = build_submission_list_admonition(exercise)

    return f'{markdown}\n\n{vscode_button}\n\n{submission_list_admonition}\n'


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
            f'<li class="exercise-list--item difficulty-{e.meta["difficulty"]}" data-slug="{e.meta["slug"]}"><a href="{base_url}{Path(e.url)}">{e.meta["title"]}</a></li>'.replace ("\\","/")
            for e in exercises
        ]
    )
    if exercises_md.strip():
        exercises_md = f'<ul class="exercise-list">\n{exercises_md}\n</ul>'
    return '\n'.join(
        re.sub(EXERCISE_LIST_REGEX, exercises_md, line)
        for line in markdown.split('\n')
    )
