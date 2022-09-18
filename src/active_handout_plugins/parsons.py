import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor
from .question import QuestionAdmonition

class ParsonsQuestion(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('question', ['parsons'], *args, **kwargs)
        self.counter = 0

    def create_question_form(self, el, submission_form):
        code = submission_form.findall('*')[-2]
        end_char = code.text.find("\x03")
        start_index = code.text.find(":") + 1
        breakpoint()
        html_idx = int(code.text[start_index:end_char])
        processed_code = self.md.htmlStash.rawHtmlBlocks[html_idx]
        
        start_index = processed_code.find("<code>") + 6

        lines = processed_code.split("\n")[:-1]
        lines[0] = lines[0][start_index:]

        print(lines)
        etreeCode = etree.fromstring(processed_code)
        
        left_panel = etree.tostring(etreeCode, encoding='unicode', method='html')
        right_panel = '''
<div class="highlight"><pre><code><p>a</p></code></pre></div>
'''
        code.set("data-pnum", str(self.counter))
        code.set("class", "parsons-code")
        code.text = self.md.htmlStash.store(left_panel + right_panel)
        breakpoint()

        self.counter += 1
        return '<input type="submit" name="sendButton" value="Enviar"/>'


