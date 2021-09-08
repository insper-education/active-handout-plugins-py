from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
from bs4 import BeautifulSoup
from collections import namedtuple
import os
import os.path as osp
import requests
from pymdownx.slugs import uslugify


PageWithExercise = namedtuple('PageWithExercise', 'slug, url, tp, topic, group')
token = os.environ.get('REPORT_TOKEN', '')


def extract_topic(url):
    split_url = url.split('/')
    if len(split_url) < 2:
        return url
    return split_url[1]


class FindExercises(BasePlugin):
    config_scheme = (
        ('report_url', mkdocs.config.config_options.Type(str, default='')),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []

    def on_files(self, files, config):
        for f in files:
            if f.src_path.endswith('meta.yml'):
                slug_url = f.url[:-len('meta.yml') + 2]
                slug_url = slug_url.replace('/', ' ').strip()
                exercise_url = '/'.join(f.url.split('/')[:-1])
                topic = extract_topic(f.url)
                self.pages_with_exercises.append(PageWithExercise(uslugify(slug_url, '-'), exercise_url, 'CODE', topic, 'handout'))

        return files

    def on_page_content(self, html, page, config, files):
        soup = BeautifulSoup(html, 'html.parser')
        page_slug = page.url.replace('/', '-')
        for idx, ex in enumerate(soup.select('.admonition.question')):
            slug = str(idx)
            for c in ex['class']:
                if c.startswith('id_'):
                    slug = c[3:]
                    break

            tp = 'QUIZ'
            if 'short' in ex['class'] or 'long' in ex['class']:
                tp = 'TEXT'

            ex['id'] = slug = page_slug + slug
            topic = extract_topic(page.url)
            self.pages_with_exercises.append(PageWithExercise(slug, page.url, tp, topic, 'handout'))

        return str(soup)

    def on_post_build(self, config):
        for slug, url, tp, topic, group in self.pages_with_exercises:
            print(slug, url, tp, topic, group)
            try:
                st = requests.post(self.config['report_url'], data={
                    'slug': slug,
                    'url': url,
                    'type': tp,
                    'topic': topic,
                    'group': group,
                }, headers={
                    'Authorization': f'Token {token}'
                })
            except Exception:
                print('enviar falhou', slug)
