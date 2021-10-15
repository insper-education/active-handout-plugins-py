import random
import string
import json
import re

### REGEX ###

def make_class_pattern(class_name=None):
    pattern = '[a-zA-Z_0-9\-]+'
    if class_name:
        pattern = class_name
    return f'\$\s*class\s+({pattern})\s*\$'


### HTML ###

def encode_html(s):
    # SOURCE: https://css-tricks.com/snippets/javascript/htmlentities-for-javascript/
    return s.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;")


def decode_html(s):
    return s.replace("&amp;", '&').replace("&lt;", '<').replace("&gt;", '>').replace("&quot;", '"')


EYE_OFF = '<span class="twemoji"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M11.83 9 15 12.16V12a3 3 0 0 0-3-3h-.17m-4.3.8 1.55 1.55c-.05.21-.08.42-.08.65a3 3 0 0 0 3 3c.22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53a5 5 0 0 1-5-5c0-.79.2-1.53.53-2.2M2 4.27l2.28 2.28.45.45C3.08 8.3 1.78 10 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.43.42L19.73 22 21 20.73 3.27 3M12 7a5 5 0 0 1 5 5c0 .64-.13 1.26-.36 1.82l2.93 2.93c1.5-1.25 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-4 .7l2.17 2.15C10.74 7.13 11.35 7 12 7z"></path></svg></span>'
EYE_ON = '<span class="twemoji"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 9a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3m0 8a5 5 0 0 1-5-5 5 5 0 0 1 5-5 5 5 0 0 1 5 5 5 5 0 0 1-5 5m0-12.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5z"></path></svg></span>'


### TEMPLATE ###

def extract_classes(template):
    return list(set(re.findall(make_class_pattern(), template)))


def render_for_display(template):
    classes = extract_classes(template)
    replacements = {c: c for c in classes}
    return apply_class_replacements(template, replacements)


def create_random_replacement(class_name, hash_len=6):
    hash_chars = string.ascii_letters + string.digits
    hash_value = "".join(random.choices(hash_chars, k=hash_len))
    return f'{class_name}-{hash_value}'


def init_class_replacements(class_names, hash_len=6):
    replacements = {}
    for class_name in class_names:
        replacements[class_name] = create_random_replacement(class_name, hash_len)
    return replacements


def extract_lines_to_hide(code):
    code = code.strip()
    lines_to_hide = []
    lines = code.split('\n')
    clean = ''
    pattern = f'\$\s*hide\s*\$'
    for i, line in enumerate(lines):
        clean_line = re.sub(pattern, '', line)
        if clean_line != line:
            lines_to_hide.append(i)
        clean += clean_line.rstrip() + '\n'
    return clean.strip(), lines_to_hide


def apply_class_replacements(template, replacements):
    for old_name, new_name in replacements.items():
        pattern = make_class_pattern(old_name)
        template = re.sub(pattern, new_name, template)
    return template


def apply_test_class_replacements(tests, replacements):
    if not tests:
        return tests
    for test in tests:
        test_class = test['testClass']
        test['testClass'] = replacements.get(test_class, test_class)
    return tests


def randomize_classes(html_template, css_template):
    classes = list(
        set(extract_classes(html_template)) |
        set(extract_classes(css_template))
    )
    replacements = init_class_replacements(classes)
    new_html = apply_class_replacements(html_template, replacements)
    new_css = apply_class_replacements(css_template, replacements)
    return new_html, new_css, replacements


def init_options(template, options):
    if not options:
        return template
    for i, option in enumerate(options):
        pattern = f'\$\s*option{i}\s*\$'
        template = re.sub(pattern, option[0]['value'], template)
    return template


def init_inputs(template):
    pattern = f'\$\s*input\s*\$'
    template = re.sub(pattern, '<input class="code-input" placeholder="Digite a resposta..." />', template)
    return template


def init_textareas(template):
    pattern = f'\$\s*textarea\s*\$'
    template = re.sub(pattern, '<textarea class="code-input" placeholder="Digite a resposta..."></textarea>', template)
    return template


def template_statement(statement):
    return f'<p>{statement}</p>'


def template_select(options):
    if not options:
        return ''
    html_options = ''.join(
        f'<option value="{option["value"]}">{option["label"]}</option>'
        for option in options
    )
    return f'<select class="combobox">{html_options}</select>'


def template_selects(option_sets):
    if not option_sets:
        return ''
    selects = ''.join(template_select(options) for options in option_sets)
    return f'<div class="css-selects">{selects}</div>'


def template_html_code(code):
    clean_code = encode_html(code.strip())
    return f'<div class="code-block"><p class="box-title tab">HTML</p><pre>{clean_code}</pre></div>'


def template_css_code(code, options, has_hidden_lines=False):
    clean_code = encode_html(init_options(code.strip(), options))
    hide_show_eyecon = f'<span class="eye-on">{EYE_ON}</span><span class="eye-off">{EYE_OFF}</span>'
    if not has_hidden_lines:
        hide_show_eyecon = ''
    return f'<div class="code-block hide-lines"><p class="box-title tab">CSS{hide_show_eyecon}</p><div class="css-code-block-container"><span class="success-check">&#10003;</span><pre class="css-code-block">{clean_code}</pre></div></div>'


def template_code_viewer(children):
    content = ''
    if children:
        content = ''.join(children)
    return f'<div class="css-code-viewer">{content}</div>'


def template_result_preview(initial_html, initial_css, expected_result):
    result_div = ''
    if expected_result:
        result_div = f'''
<div class="html-preview">
  <p class="box-title">Esperado</p>
  <div class="preview-container">{expected_result}</div>
</div>
'''.strip()
    return f'''
<div class="style-container">
  <style>{initial_css}</style>
  <div class="html-preview">
    <p class="box-title">Resultado</p>
    <div class="preview-container">{initial_html}</div>
  </div>
  {result_div}
</div>
'''.strip()


def template_viewer_container(title, is_question, tests, display_html, display_css, fixed_class_html, fixed_class_css, html_lines_to_hide, css_lines_to_hide, children):
    content = ''
    if children:
        content = ''.join(children)

    tests_json = ""
    if tests:
        tests_json = json.dumps(tests)

    return (
        f'<div class="css-exercise admonition {"question" if is_question else "info"}" ' +
            f'data-tests="{encode_html(tests_json)}" ' +
            f'data-html-block="{encode_html(fixed_class_html)}" ' +
            f'data-css-block="{encode_html(fixed_class_css)}" ' +
            f'data-html-code-block="{encode_html(display_html)}" ' +
            f'data-css-code-block="{encode_html(display_css)}"' +
            f'data-html-lines-to-hide="{html_lines_to_hide}"' +
            f'data-css-lines-to-hide="{css_lines_to_hide}"' +
            f'>' +
          f'<p class="admonition-title">{title}</p>' +
          content +
        '</div>'
    )
