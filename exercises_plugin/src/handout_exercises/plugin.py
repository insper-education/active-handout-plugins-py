from pathlib import Path
from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
import os

from .exercise import add_vscode_button, find_code_exercises, find_exercises_in_handout, is_exercise_list, get_meta_for, post_exercises, replace_exercise_list, sorted_exercise_list


token = os.environ.get('REPORT_TOKEN', '')


class FindExercises(BasePlugin):
    config_scheme = (
        ('offering_id', mkdocs.config.config_options.Type(int, default=-1)),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []
        self.code_exercises_by_path = {}

    def on_files(self, files, config):
        code_exercises = find_code_exercises(files, self.config['offering_id'])
        self.pages_with_exercises.extend(code_exercises)
        self.code_exercises_by_path = {ex.meta_file.abs_src_path: ex for ex in code_exercises}
        return files

    def on_page_markdown(self, markdown, page, config, files):
        if is_exercise_list(markdown):
            exercises = sorted_exercise_list(
                page.file.abs_src_path,
                self.code_exercises_by_path
            )
            return replace_exercise_list(markdown, exercises, config['site_url'])

        meta_file = get_meta_for(page.file, files)
        if meta_file:
            return add_vscode_button(markdown, meta_file, config['site_url'])

        return markdown

    def on_page_content(self, html, page, config, files):
        new_exercises, new_html = find_exercises_in_handout(html, page.url, page.file.abs_src_path, self.code_exercises_by_path)
        self.pages_with_exercises.extend(new_exercises)
        return new_html

    def on_post_build(self, config):
        try:
            report_url = config['extra']['ihandout_config']['report']['url']
            post_exercises(self.pages_with_exercises, token, report_url)
        except:
            pass

        for exercise in self.code_exercises_by_path.values():
            exercise.save_meta()
