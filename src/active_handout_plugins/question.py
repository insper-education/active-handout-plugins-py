import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor


class QuestionAdmonition(AdmonitionVisitor):
    def __init__(self, classes, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.classes = classes
        self.counter = 0

    def visit(self, el):
        if 'question' not in el.attrib['class']:
            return

        cls = self.has_class(el, self.classes)
        
        if not cls:
            return

        self.counter += 1
        el.set("id", f"{cls}-{self.counter}")

        title = el.find('p/[@class="admonition-title"]')
        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            answer.attrib['style'] = 'display: none;'

        content = []
        for child in el:
            if child == title or child == answer:
                continue
            
            content.append(child)
        
        submission_form = etree.SubElement(el, 'form')
        hs_code = '''
on submit
    halt the event
    show the <.answer/> in me
    add @disabled to <input/> in me
    hide the <input[type="submit"]/> in me
    send remember(element: me) to window
end
        '''
        submission_form.set('_', hs_code)

        for par in content:
            el.remove(par)
            submission_form.append(par)

        form_elements = etree.SubElement(submission_form, 'div')
        form_elements.set("class", "form-elements")
        html_elements = self.create_question_form(el, submission_form)
        form_elements.text = self.md.htmlStash.store(html_elements)

        if answer:
            el.remove(answer)
            submission_form.append(answer)
    
    def create_question_form(self, el, submission_form):
        return ''


class ChoiceQuestion(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(['choice'], *args, **kwargs)
    
    def create_question_form(self, el, submission_form):
        choice_list = submission_form.find(".//ul[@class='task-list']")
        choices = submission_form.findall(".//ul[@class='task-list']/li")
        submission_form.remove(choice_list)

        html_elements = ''
        for i, choice in enumerate(choices):
            end = choice.text.find('\x03')
            html_elements += f'<label><input type="radio" name="data" value="{i}"> {choice.text[end:]}  </label>\n'
        html_elements += '<input type="submit" name="sendButton" value="Enviar"/>'

        return html_elements
        

class TextQuestion(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(['short', 'medium', 'long'], *args, **kwargs)

    def create_question_form(self, el, submission_form):
        return f'''
<input type="text" value="" name="data"/>

<input type="submit" value="Enviar"/>
'''
    