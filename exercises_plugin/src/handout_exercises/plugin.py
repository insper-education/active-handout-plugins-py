from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
import os

from .exercise import find_code_exercises, find_exercises_in_handout, post_exercises


token = os.environ.get('REPORT_TOKEN', '')

class FindExercises(BasePlugin):
    config_scheme = (
        ('report_url', mkdocs.config.config_options.Type(str, default='')),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []

    def on_files(self, files, config):
        self.pages_with_exercises.extend(find_code_exercises(files))
        return files

    def on_page_content(self, html, page, config, files):
        new_exercises, new_html = find_exercises_in_handout(html, page.url)
        self.pages_with_exercises.extend(new_exercises)
        return new_html

    def on_post_build(self, config):
        post_exercises(self.pages_with_exercises, token, self.config['report_url'])
