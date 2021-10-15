from css_exercises.plugin_helper import load_local_file
from css_exercises.template_utils import apply_test_class_replacements, extract_lines_to_hide, init_inputs, init_options, init_textareas, randomize_classes, render_for_display, template_code_viewer, template_css_code, template_html_code, template_result_preview, template_selects, template_statement, template_viewer_container
from mkdocs.plugins import BasePlugin
import yaml
import re


def parse_viewer(viewer_data, page, files):
    data = yaml.safe_load(viewer_data)
    data['expected'] = load_local_file(data.get('expected'), page, files)
    data['html'] = load_local_file(data.get('html'), page, files)
    data['css'] = load_local_file(data.get('css'), page, files)
    data.setdefault('question', True)
    return data


def process_viewer(viewer_data, page, files):
    data = parse_viewer(viewer_data, page, files)
    html, html_lines_to_hide = extract_lines_to_hide(data['html'])
    css, css_lines_to_hide = extract_lines_to_hide(data['css'])
    display_html = render_for_display(html)
    display_css = render_for_display(css)
    fixed_class_html, fixed_class_css, replacements = randomize_classes(html, css)
    tests = apply_test_class_replacements(data.get('tests'), replacements)
    options = data.get('options')

    return template_viewer_container(
        data.get('title'),
        data['question'],
        tests,
        display_html,
        init_textareas(init_inputs(display_css)),
        fixed_class_html,
        fixed_class_css,
        html_lines_to_hide,
        css_lines_to_hide, [
            template_statement(data.get('statement')),
            template_selects(options),
            template_code_viewer([
                template_html_code(display_html),
                init_textareas(init_inputs(template_css_code(display_css, options, len(css_lines_to_hide) > 0))),
            ]),
            template_result_preview(
                init_options(fixed_class_html, options),
                init_options(fixed_class_css, options),
                data.get('expected')
            ),
        ])


class CreateExercises(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        new_md = ''
        in_viewer = False
        tabs = None
        viewer_data = ''
        for line in markdown.split('\n'):
            line += '\n'
            if '!!!' in line and 'cssviewer' in line:
                in_viewer = True
                tabs = None
                viewer_data = ''
            elif in_viewer:
                if tabs is None:
                    matches = re.match('(^[ \t]+)', line)
                    if matches is not None:
                        tabs = matches.group()
                        viewer_data += line
                else:
                    matches = re.match(f'(^(?!{tabs}))', line)
                    if matches and not line.strip():
                        viewer = process_viewer(viewer_data, page, files)
                        new_md += viewer
                        in_viewer = False
                    else:
                       viewer_data += line
            if not in_viewer:
                new_md += line
        if in_viewer:
            viewer = process_viewer(viewer_data, page, files)
            new_md += viewer
        return new_md
