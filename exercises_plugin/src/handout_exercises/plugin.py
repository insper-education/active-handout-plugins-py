from pathlib import Path
from mkdocs.plugins import BasePlugin
import mkdocs.config.config_options
import os

from .exercise import add_authors, get_title, add_vscode_button, find_code_exercises, find_exercises_in_handout, is_exercise_list, get_meta_for, post_exercises, replace_exercise_list, sorted_exercise_list, override_yaml


token = os.environ.get('REPORT_TOKEN', '')


class FindExercises(BasePlugin):
    config_scheme = (
        ('report_url', mkdocs.config.config_options.Type(str, default='')),
    )

    def on_pre_build(self, config):
        self.pages_with_exercises = []
        self.yaml_overrides = {}
        self.code_exercises_by_path = {}

    def on_files(self, files, config):
        code_exercises = find_code_exercises(files)
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
            self.yaml_overrides[meta_file.abs_dest_path] = {
                'title': get_title(markdown)
            }
            new_markdown = add_vscode_button(markdown, meta_file, config['site_url'])
            project_root = Path(config['config_file_path']).parent
            return add_authors(new_markdown, self.code_exercises_by_path[meta_file.abs_src_path], project_root)

        return markdown

    def on_page_content(self, html, page, config, files):
        new_exercises, new_html = find_exercises_in_handout(html, page.url)
        self.pages_with_exercises.extend(new_exercises)
        return new_html

    def on_post_build(self, config):
        post_exercises(self.pages_with_exercises, token, self.config['report_url'])
        for abs_dest_path, overrides in self.yaml_overrides.items():
            override_yaml(abs_dest_path, overrides)
