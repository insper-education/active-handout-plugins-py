from unittest.mock import patch
from css_exercises.template_utils import apply_class_replacements, extract_lines_to_hide, init_inputs, init_textareas, randomize_classes, render_for_display, template_code_viewer, template_css_code, template_html_code, template_result_preview, template_select, decode_html, encode_html, extract_classes, template_selects, init_class_replacements, init_options, template_viewer_container
from bs4 import BeautifulSoup

DECODED = '''
    <div class="container">
      <p id="paragraph-id">Lorem ipsum</p>
    </div>
'''
ENCODED = '''
    &lt;div class=&quot;container&quot;&gt;
      &lt;p id=&quot;paragraph-id&quot;&gt;Lorem ipsum&lt;/p&gt;
    &lt;/div&gt;
'''
HTML_TEMPLATE = '''
<div class="$class parent$">
  <div class="$class child$">A</div>
  <div class="$class child$">B</div>
  <div class="$class child$ $ class special $">C</div>
</div>
'''
CSS_TEMPLATE = '''
.$class parent$ {
  display: flex;
  flex-direction: $option0$;
  width: 15rem;
  height: 15rem;
  margin: 0.1rem 0 1rem;
  padding: 0.5rem;
  background-color: silver;
}

.$class child$ {
  margin: 0.5rem;
  padding: 0.5rem;
  background-color: gold;
}

.$  class  other-class  $ {
  border: 1px solid black;
}
'''


def test_encode_and_decode_html():
    assert DECODED == decode_html(ENCODED)
    assert ENCODED == encode_html(DECODED)


def test_extract_classes():
    tests = [
        (HTML_TEMPLATE, ['special', 'parent', 'child']),
        (CSS_TEMPLATE, ['other-class', 'parent', 'child']),
    ]
    for template, expected_names in tests:
        class_names = extract_classes(template)
        assert len(class_names) == len(expected_names)
        assert set(expected_names) == set(class_names)


def test_init_replacements():
    class_names = ['parent', 'child', 'special', 'other-class']
    hash_len = 5
    replacements = init_class_replacements(class_names, hash_len=hash_len)
    assert len(class_names) == len(replacements)
    for class_name in class_names:
        new_name = replacements[class_name]
        assert new_name.startswith(f'{class_name}-')
        assert len(new_name) == len(class_name) + hash_len + 1


def test_render_for_display():
    tests = [
        (HTML_TEMPLATE, '''
<div class="parent">
  <div class="child">A</div>
  <div class="child">B</div>
  <div class="child special">C</div>
</div>
'''),
        (CSS_TEMPLATE, '''
.parent {
  display: flex;
  flex-direction: $option0$;
  width: 15rem;
  height: 15rem;
  margin: 0.1rem 0 1rem;
  padding: 0.5rem;
  background-color: silver;
}

.child {
  margin: 0.5rem;
  padding: 0.5rem;
  background-color: gold;
}

.other-class {
  border: 1px solid black;
}
''')
    ]
    for template, expected in tests:
        assert expected == render_for_display(template)


def test_apply_replacements():
    replacements = {
        'parent': 'parent-abc123',
        'child': 'child-def456',
        'special': 'special-ghi789',
        'other-class': 'other-classjkl101',
    }
    replaced_html = f'''
<div class="{replacements["parent"]}">
  <div class="{replacements["child"]}">A</div>
  <div class="{replacements["child"]}">B</div>
  <div class="{replacements["child"]} {replacements["special"]}">C</div>
</div>
'''
    replaced_css = f'''
.{replacements["parent"]} {{
  display: flex;
  flex-direction: $option0$;
  width: 15rem;
  height: 15rem;
  margin: 0.1rem 0 1rem;
  padding: 0.5rem;
  background-color: silver;
}}

.{replacements["child"]} {{
  margin: 0.5rem;
  padding: 0.5rem;
  background-color: gold;
}}

.{replacements["other-class"]} {{
  border: 1px solid black;
}}
'''
    tests = [
        (HTML_TEMPLATE, replaced_html),
        (CSS_TEMPLATE, replaced_css),
    ]
    for template, expected in tests:
        replaced = apply_class_replacements(template, replacements)
        assert replaced == expected


def test_init_options():
    css_template = '''
.$class selector$ {
  display: $option1$;
  $option0$
}
'''
    html_template = '''
<p class="$ class selector $">
  $ option1 $
</p>
'''
    options = [
        [
            {
                'value': 'padding: 1rem;',
                'label': 'Padding',
            },
            {
                'value': 'margin: 1rem;',
                'label': 'Margin',
            },
        ],
        [
            {
                'value': 'flex',
                'label': 'Flex',
            },
            {
                'value': 'block',
                'label': 'Block',
            },
        ],
    ]
    css_with_options = css_template.replace('$option0$', 'padding: 1rem;').replace('$option1$', 'flex')
    html_with_options = html_template.replace('$ option1 $', 'flex')
    assert init_options(css_template, options) == css_with_options
    assert init_options(html_template, options) == html_with_options


def test_init_inputs():
    css_template = '''
.$class selector$ {
  display: $input$;
  justify-content: $   input     $;
  $option0$
}
'''
    expected = '''
.$class selector$ {
  display: <input class="code-input" placeholder="Digite a resposta..." />;
  justify-content: <input class="code-input" placeholder="Digite a resposta..." />;
  $option0$
}
'''
    assert init_inputs(css_template) == expected


def test_init_textareas():
    css_template = '''
.$class selector$ {
  $textarea$;
  $   textarea     $;
  $option0$
}
'''
    expected = '''
.$class selector$ {
  <textarea class="code-input" placeholder="Digite a resposta..."></textarea>;
  <textarea class="code-input" placeholder="Digite a resposta..."></textarea>;
  $option0$
}
'''
    assert init_textareas(css_template) == expected


def test_template_select():
    options = [
        {
            'value': 'flex',
            'label': 'Flex',
        },
        {
            'value': 'block',
            'label': 'Block',
        },
    ]
    soup = BeautifulSoup(template_select(options), features='html.parser')
    select = soup.find('select', class_='combobox')
    options = select.find_all('option')
    assert len(options) == 2
    assert options[0].get('value') == 'flex'
    assert options[0].text == 'Flex'
    assert options[1].get('value') == 'block'
    assert options[1].text == 'Block'


def test_empty_template_select():
    assert template_select(None) == ''


def test_template_selects():
    selects_data = [
        [
            {
                'value': 'padding: 1rem;',
                'label': 'Padding',
            },
            {
                'value': 'margin: 1rem;',
                'label': 'Margin',
            },
        ],
        [
            {
                'value': 'flex',
                'label': 'Flex',
            },
            {
                'value': 'block',
                'label': 'Block',
            },
        ],
    ]
    soup = BeautifulSoup(template_selects(selects_data), features='html.parser')
    select_container = soup.find('div', class_='css-selects')
    selects = select_container.find_all('select', class_='combobox')
    assert len(selects) == len(selects_data)
    for select, select_data in zip(selects, selects_data):
        options = select.find_all('option')
        assert len(options) == len(select_data)
        for option, option_data in zip(options, select_data):
            assert option.get('value') == option_data['value']
            assert option.text == option_data['label']


def test_empty_template_selects():
    assert template_selects(None) == ''


def test_template_html_code():
    code = '''
      <div>
  <p>Text</p>
</div>  '''
    soup = BeautifulSoup(template_html_code(code), features='html.parser')
    code_block = soup.find('div', class_='code-block')
    assert code_block.find('p', class_='box-title').text == 'HTML'
    # template_html_code encodes the HTML and BS4 decodes it, so the
    # text should be the same except for the leading and trailling white spaces.
    assert code_block.find('pre').text == code.strip()


def test_template_css_code():
    options = [[
        {'value': '1rem', 'label': 'small'},
        {'value': '3rem', 'label': 'large'},
    ]]
    code = '''
.container {
  margin: $ option0 $;
}
    '''
    expected = '''.container {
  margin: 1rem;
}'''
    soup = BeautifulSoup(template_css_code(code, options), features='html.parser')
    code_block = soup.find('div', class_='code-block')
    assert code_block.find('p', class_='box-title').text == 'CSS'
    assert code_block.find('pre').text == expected


def test_template_css_code_with_empty_options():
    code = '''
.container {
  margin: $input$;
}
    '''
    expected = code.strip()
    soup = BeautifulSoup(template_css_code(code, None), features='html.parser')
    code_block = soup.find('div', class_='code-block')
    assert code_block.find('p', class_='box-title').text == 'CSS'
    assert code_block.find('pre').text == expected


def test_extract_lines_to_hide():
    code = '''
.container {
  margin: $input$;
  width: 10px; $ hide  $
  height: 10px; $hide$
}
'''
    expected = '''.container {
  margin: $input$;
  width: 10px;
  height: 10px;
}'''
    clean_code, lines = extract_lines_to_hide(code)
    assert lines == [2, 3]
    assert clean_code == expected


def test_template_code_viewer():
    soup = BeautifulSoup(template_code_viewer(['<p>Text</p>', '<span>More text</span>']), features='html.parser')
    code_block = soup.find('div', class_='css-code-viewer')
    assert code_block.find('p').text == 'Text'
    assert code_block.find('span').text == 'More text'


def test_template_result_preview():
    html = '''<p>
  Test
</p>'''
    css = '''.container {
  margin: 1rem;
}'''
    soup = BeautifulSoup(template_result_preview(html, css, ''), features='html.parser')
    style_container = soup.find('div', class_='style-container')
    style_container.find('style').text == css
    preview_container = style_container.find('div', class_='html-preview')
    preview_container.find('p', class_='box-title').text == 'Resultado'
    preview_container.find('div').find('p').text == 'Test'


def mock_create_random_replacement(class_name, *args):
    return f'{class_name}-asd123'
@patch('css_exercises.template_utils.create_random_replacement', side_effect=mock_create_random_replacement)
def test_template_viewer_container(mocked_function):
    html_template = '<div class="$class foo$">\n  bar\n</div>'
    css_template = '.$class foo$ {\n  margin: 1rem;\n}'
    display_html = render_for_display(html_template)
    display_css = render_for_display(css_template)
    fixed_class_html, fixed_class_css, _ = randomize_classes(html_template, css_template)

    soup = BeautifulSoup(
        template_viewer_container(
            'Title',
            True,
            None,
            display_html,
            display_css,
            fixed_class_html,
            fixed_class_css,
            [],
            [],
            ['<span class="child">Text</span>']),
        features='html.parser'
    )
    container = soup.find('div', class_='css-exercise')
    assert container.attrs['data-html-block'] == fixed_class_html
    assert container.attrs['data-css-block'] == fixed_class_css
    assert container.attrs['data-html-code-block'] == display_html
    assert container.attrs['data-css-code-block'] == display_css
    assert container.find('p', class_='admonition-title').text == 'Title'
    assert container.find('span', class_='child').text == 'Text'
