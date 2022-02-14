from handout_exercises.navigation import add_missing_nav_parents
from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
import os

from .exercise import enhance_exercise_md, export_exercises_file, find_code_exercises, find_exercises_in_handout, is_exercise_list, get_meta_for, post_exercises, replace_exercise_list, sorted_exercise_list


token = os.environ.get('REPORT_TOKEN', '')


class FindExercises(BasePlugin):
    config_scheme = (
        ('offering_id', mkdocs.config.config_options.Type(int, default=-1)),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []
        self.code_exercises_by_path = {}

    def on_files(self, files, config):
        exercise_candidates = [f for f in files if not f.src_path.startswith('agradecimentos')]
        code_exercises = find_code_exercises(exercise_candidates, self.config['offering_id'])
        self.pages_with_exercises.extend(code_exercises)
        self.code_exercises_by_path = {ex.meta_file.abs_src_path: ex for ex in code_exercises}
        return files

    def on_nav(self, nav, config, files):
        return add_missing_nav_parents(nav, files)

    def on_page_markdown(self, markdown, page, config, files):
        if is_exercise_list(markdown):
            exercises = sorted_exercise_list(
                page.file.abs_src_path,
                self.code_exercises_by_path
            )
            return replace_exercise_list(markdown, exercises, config['site_url'])

        meta_file = get_meta_for(page.file, files)
        if meta_file:
            exercise = self.code_exercises_by_path[meta_file.abs_src_path]
            return enhance_exercise_md(exercise, markdown, meta_file, config['site_url'])

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

        export_exercises_file(self.pages_with_exercises, config['site_dir'])
