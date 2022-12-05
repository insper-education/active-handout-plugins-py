from .exercise import ExerciseAdmonition
import random
import xml.etree.ElementTree as etree
import json

class ParsonsExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['parsons'], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        code = submission_form.findall('*')[-2]
        end_char = code.text.find("\x03")
        start_index = code.text.find(":") + 1
        html_idx = int(code.text[start_index:end_char])
        processed_code = self.md.htmlStash.rawHtmlBlocks[html_idx]

        start_index = processed_code.find("<code>") + 6
        lines = processed_code.split("\n")[:-1]
        lines[0] = lines[0][start_index:]

        random.shuffle(lines)
        left_panel = '''
<div class="parsons-container highlight original-code">
    <pre><code class="parsons-area parsons-drag-area">
'''
        for l in lines:
            indent_count = l.count('    ')
            l_no_indent = l.replace('    ', '')
            left_panel += f'''
<div class="line-slot with-line">
    <div class="subslot cur-indent single-subslot"></div>
    <div class="line-placeholder"></div>
    <div class="parsons-line" draggable="true" data-indentCount={indent_count}>{l_no_indent}</div>
</div>
'''
        left_panel += '</code></pre></div>'

        right_panel = '''
<div class="parsons-container highlight parsons-drop-div">
    <pre><code class="parsons-area parsons-drop-area"></code></pre>
</div>
'''
        code.set("class", "parsons-code")
        code.tag = 'div'
        code.text = self.md.htmlStash.store(left_panel + right_panel)

        parse_html = etree.fromstring(processed_code)
        full_answer = "".join(parse_html.itertext())
        return f'''
        <input type="hidden" name="data" value=""/>
        <pre class="parsons-answer">{full_answer}</pre>
        <div class="ah-btn-group">
            <input type="button" class="ah-button ah-button--primary" name="resetButton" value="Reset"/>
            <input type="button" class="ah-button ah-button--primary" name="sendButton" value="Testar"/>
        </div>
        '''

    def create_answer(self):
        return f'''
<p class="admonition-title">Resposta</p>
<p class="wrong-answer">Wrong answer</p>
<p class="correct-answer">Correct answer</p>
'''
