from bs4 import BeautifulSoup
from pymdownx.slugs import slugify
import requests


HANDOUT_GROUP = 'handout'
CODE_TYPE = 'CODE'
QUIZ_TYPE = 'QUIZ'
TEXT_TYPE = 'TEXT'


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
            exercise_url = '/'.join(f.url.split('/')[:-1])
            topic = extract_topic(f.url)
            exercises.append(Exercise(slugify()(slug_url, '-'), exercise_url, CODE_TYPE, topic, HANDOUT_GROUP))

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

