import re
from .l10n import gettext as _
from .exercise import ExerciseAdmonition


class CSSExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['css-exercise'], *args, **kwargs)

    def __find_code_html(self, code_element):
        if code_element is None or not code_element.text:
            return None

        end_char = code_element.text.find("\x03")
        start_index = code_element.text.find(":") + 1
        try:
            html_idx = int(code_element.text[start_index:end_char])
        except ValueError:
            return None

        return self.md.htmlStash.rawHtmlBlocks[html_idx]

    def __extract_code(self, code_html):
        return re.sub('<[^>]+>', '', code_html)

    def __extract_language(self, code_html):
        match = re.match(r'<div[^>]*language-(\S*)[^>]*>', code_html)
        if match:
            return match.group(1)
        return 'raw'

    def __extract_filename(self, code_html):
        match = re.match(r'<div[^>]*filename-(\S*)[^>]*>', code_html)
        if match:
            return match.group(1)
        return 'index'

    def __is_hidden(self, code_html):
        return bool(re.match(r'<div[^>]*hidden-file(\S*)[^>]*>', code_html))

    def __create_playground(self, files):
        editors = ''
        filenames = ''
        is_first = True
        for filename, file_data in files.items():
            tab_classes = 'tab'
            editor_classes = 'playground-code-editor'
            if file_data['is_hidden']:
                editor_classes += ' hidden-file'
            else:
                if is_first:
                    tab_classes += ' active'
                    editor_classes += ' active'
                is_first = False

                filenames += f'<li class="{ tab_classes }">{ filename }</li>'
            editors += f'<div class="{ editor_classes }" data-language="{ file_data["language"] }" data-filename="{ filename }">{ file_data["code"] }</div>'

        preview_str = _('Preview')
        expected_str = _('Expected')

        return f'''
<div class="css-playground">
    <div class="file-editor">
        <ul class="file-tab">{filenames}</ul>
        { editors }
    </div>
    <div class="page-preview">
        <p>{ preview_str }</p>
        <iframe class="preview"></iframe>
        <p>{ expected_str }</p>
        <iframe class="expected-result"></iframe>
    </div>
</div>
'''

    def create_exercise_form(self, el, submission_form):
        files = {}
        for code_element in submission_form.findall('*'):
            code_html = self.__find_code_html(code_element)
            if code_html:
                code = self.__extract_code(code_html)
                language = self.__extract_language(code_html)
                filename = f'{self.__extract_filename(code_html)}.{language}'
                is_hidden = self.__is_hidden(code_html)
                files[filename] = {
                    'code': code,
                    'is_hidden': is_hidden,
                    'language': language,
                }

                submission_form.remove(code_element)

        reset_str = _('Reset')
        test_str = _('Test')

        return f'''
        {self.__create_playground(files)}
        <input type="hidden" name="data" value=""/>
        <div class="ah-btn-group">
            <input type="button" class="ah-button ah-button--primary reset-css" name="resetButton" value="{ reset_str }"/>
            <input type="button" class="ah-button ah-button--primary test-css" name="sendButton" value="{ test_str }"/>
        </div>
        '''
