import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor


class QuestionAdmonition(AdmonitionVisitor):
    def __init__(self, base_class, subclasses, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.subclasses = subclasses
        self.base_class = base_class
        self.counter = 0

    def __set_element_id(self, el, cls):
        self.counter += 1
        el.set("id", f"{cls}-{self.counter}")
        classes = el.attrib['class'].split()
        for c in classes:
            if c.startswith('id_'):
                el.set("id", c[3:])
                el.attrib['class'] = el.attrib['class'].replace(c, '')

    def __add_question_description(self, el, submission_form):
        title = el.find('p/[@class="admonition-title"]')
        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            answer.attrib['style'] = 'display: none;'

        content = []
        for child in el:
            if child == title or child == answer or child == submission_form:
                continue

            content.append(child)

        for par in content:
            el.remove(par)
            submission_form.append(par)

    def __add_question_form_elements(self, el, submission_form):
        form_elements = etree.SubElement(submission_form, 'div')
        form_elements.set("class", "form-elements")
        html_elements = self.create_question_form(el, submission_form)
        form_elements.text = self.md.htmlStash.store(html_elements)

        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            el.remove(answer)
            submission_form.append(answer)


    def visit(self, el):
        if self.base_class not in el.attrib['class']:
            return

        cls = self.base_class
        if self.subclasses:
            cls = self.has_class(el, self.subclasses)
            if not cls:
                return

        self.__set_element_id(el, cls)
        submission_form = etree.SubElement(el, 'form')
        self.__add_question_description(el, submission_form)
        hs_code = '''
on submit
    halt the event
    if <.answer/>
        show the <.answer/> in me
    end
    add @disabled to <input/> in me
    add .done to me
    hide the <input[type="submit"]/> in me
    send remember(element: my parentElement) to window
end
        '''
        submission_form.set('_', hs_code)
        self.__add_question_form_elements(el, submission_form)

    def create_question_form(self, el, submission_form):
        return ''


class ChoiceQuestion(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('question', ['choice'], *args, **kwargs)
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
        super().__init__('question', ['short', 'medium', 'long'], *args, **kwargs)

    def create_question_form(self, el, submission_form):
        if self.has_class(el, 'short'):
            text_widget = '<input type="text" value="" name="data"/>'
        elif self.has_class(el, 'medium'):
            text_widget = '<textarea name="data"></textarea>'
        if self.has_class(el, 'long'):
            text_widget = '<textarea name="data"></textarea>'
        return f'''
{text_widget}

<input type="submit" value="Enviar"/>
'''

