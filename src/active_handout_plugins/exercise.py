import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor


class ExerciseAdmonition(AdmonitionVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__visitors = []
    
    def register(self, visitor, weight):
        self.__visitors.append((weight, visitor))
        self.__visitors.sort()
    
    @property
    def visitors(self):
        for _, v in self.__visitors:
            yield v
    
    def __select_visitor(self, el):
        """Return the first match based on the priority"""

        for visitor in self.visitors:
            cls = visitor.base_class
            if cls not in el.attrib['class']:
                continue

            if visitor.subclasses:
                cls = self.has_class(el, visitor.subclasses)
                if not cls:
                    continue
            
            return visitor, cls
        return None, None

    def visit(self, el):
        visitor, cls = self.__select_visitor(el)
        if visitor:
            visitor.visit(el, cls)


class ExerciseAdmonitionVisitor:
    def __init__(self, base_class, subclasses, md) -> None:
        self.md = md
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

    def __add_exercise_description(self, el, submission_form):
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

    def __add_exercise_form_elements(self, el, submission_form):
        form_elements = etree.SubElement(submission_form, 'div')
        form_elements.set("class", "form-elements")
        html_elements = self.create_exercise_form(el, submission_form)
        form_elements.text = self.md.htmlStash.store(html_elements)

        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            el.remove(answer)
            submission_form.append(answer)


    def visit(self, el, cls):
        self.__set_element_id(el, cls)
        submission_form = etree.SubElement(el, 'form')
        self.__add_exercise_description(el, submission_form)
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
        self.__add_exercise_form_elements(el, submission_form)
    

    def create_exercise_form(self, el, submission_form):
        return ''


class ChoiceExercise(ExerciseAdmonitionVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['choice'], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        choice_list = submission_form.find(".//ul[@class='task-list']")
        choices = submission_form.findall(".//ul[@class='task-list']/li")
        submission_form.remove(choice_list)

        html_elements = ''
        for i, choice in enumerate(choices):
            end = choice.text.find('\x03')
            html_elements += f'<label><input type="radio" name="data" value="{i}"> {choice.text[end:]}  </label>\n'
        html_elements += '<input type="submit" name="sendButton" value="Enviar"/>'

        return html_elements


class TextExercise(ExerciseAdmonitionVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['short', 'medium', 'long'], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
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


class SelfProgressExercise(ExerciseAdmonitionVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', [], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        return '''
<input type="hidden" name="data" value="OK" />
<input type="submit" name="enviar" value="Marcar como feito" />
'''
