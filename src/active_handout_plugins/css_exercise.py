import re
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
        match = re.match('<div[^>]*language-(\S*)[^>]*>', code_html)
        if match:
            return match.group(1)
        return 'raw'

    def __create_playground(self, files):
        editors = ''
        filenames = ''
        for i, (language, code) in enumerate(files.items()):
            filename = f'index.{language}'
            tab_classes = 'tab'
            editor_classes = 'playground-code-editor'
            if i == 0:
                tab_classes += ' active'
                editor_classes += ' active'
            filenames += f'<li class="{ tab_classes }">{ filename }</li>'
            editors += f'<div class="{ editor_classes }" data-language="{ language }" data-filename="{ filename }">{ code }</div>'
        return f'''
<div class="css-playground">
    <ul class="file-tab">{filenames}</ul>
    { editors }
    <div class="page-preview"><iframe></div>
</div>
'''

    def create_exercise_form(self, el, submission_form):
        files = {}
        for code_element in submission_form.findall('*'):
            code_html = self.__find_code_html(code_element)
            if code_html:
                code = self.__extract_code(code_html)
                language = self.__extract_language(code_html)
                files[language] = code

                submission_form.remove(code_element)

        return f'''
        {self.__create_playground(files)}
        <input type="hidden" name="data" value=""/>
        <div class="ah-btn-group">
            <input type="button" class="ah-button ah-button--primary" name="resetButton" value="Reset"/>
            <input type="button" class="ah-button ah-button--primary" name="sendButton" value="Testar"/>
        </div>
        '''
