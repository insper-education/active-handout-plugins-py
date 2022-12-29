import xml.etree.ElementTree as etree
from .l10n import gettext as _
from .admonition import AdmonitionVisitor
import random


class ExerciseAdmonition(AdmonitionVisitor):
    def __init__(self, base_class, subclasses, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.base_class = base_class
        self.subclasses = subclasses
        self.counter = 0
        self.id = ''

    def __set_element_id(self, el, cls):
        self.counter += 1
        self.id = f"{cls}_{self.counter}"
        classes = el.attrib['class'].split()
        for c in classes:
            if c.startswith('id_'):
                self.id = '{c[3:]}'
                el.attrib['class'] = el.attrib['class'].replace(c, '')
        
        el.set("id", self.id)

    def __set_tags(self, el):
        tags = self.get_tags(el)
        for tag in tags:
            el.attrib['class'] += f' tag-{tag}'


    def __add_exercise_description(self, el, submission_form):
        title = el.find('p/[@class="admonition-title"]')
        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            answer.attrib['style'] = 'display: none;'
            answer_title = answer.find('p/[@class="admonition-title"]')
            answer_title.text = _(answer_title.text)

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
        else:
            answer_content = self.create_answer()
            if answer_content:
                answer = etree.SubElement(submission_form, 'div')
                answer.set("class", "admonition answer")
                answer.set("style", "display: none;")
                answer.text = self.md.htmlStash.store(answer_content)

    def __match_class(self, el):
        cls = self.base_class
        if cls not in el.attrib['class']:
            return None

        if self.subclasses:
            return self.has_class(el, self.subclasses)

        return cls

    def match(self, el):
        return bool(self.__match_class(el))

    def visit(self, el):
        cls = self.__match_class(el)
        self.__set_element_id(el, cls)
        self.__set_tags(el)
        self.add_extra_classes(el)
        submission_form = etree.SubElement(el, 'form')
        self.__add_exercise_description(el, submission_form)
        hs_code = '''
on submit
    halt the event
    if <.answer/>
        show the <.answer/> in me
    end
    add @disabled to <input/> in me
    add @disabled to <textarea/> in me
    add .done to closest .exercise
    hide the <input[type="submit"]/> in me
    send remember(element: my parentElement) to window
end
        '''
        submission_form.set('_', hs_code)
        self.__add_exercise_form_elements(el, submission_form)


    def create_exercise_form(self, el, submission_form):
        return ''

    def add_extra_classes(self, el):
        return

    def create_answer(self):
        return ''

    def get_tags(self, el):
        return []


class ChoiceExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['choice'], *args, **kwargs)

    def __is_answer(self, stash_key):
        key = int(stash_key[stash_key.index(':')+1:])
        return 'checked' in self.md.htmlStash.rawHtmlBlocks[key]

    def create_exercise_form(self, el, submission_form):
        choice_list = submission_form.find(".//ul[@class='task-list']")
        choices = submission_form.findall(".//ul[@class='task-list']/li")
        submission_form.remove(choice_list)

        html_alternatives = []
        answer_idx = -1

        submit_str = _('Submit')

        for i, choice in enumerate(choices):
            end = choice.text.find('\x03') + 1
            is_answer = self.__is_answer(choice.text[:end-1])
            if is_answer:
                answer_idx = i
            text = choice.text[end:]
            if text.startswith('*'):
                text = text[1:]
            content = text + ''.join(etree.tostring(e, 'unicode') for e in choice if e.tag != 'label')
            script = '''
            on click
                set alternative to closest .alternative
                if alternative matches <:not(.selected)/> then
                    set selected to false
                else
                    set selected to true
                end
                remove .selected from .alternative in closest .alternative-set
                if selected then
                    remove .selected from alternative
                    add @disabled to <input[type='submit']/> in closest .form-elements
                else
                    add .selected to alternative
                    remove @disabled from <input[type='submit']/> in closest .form-elements
                end
            end
            '''.replace('\n', '').replace('    ', ' ')
            html_alternatives.append(f'''
<label class="alternative">
  <div class="content">
    <input type="radio" name="data" value="{i}" _="{script}">
    {content}
  </div>
</label>
''')

        random.shuffle(html_alternatives)
        el.set('data-answer-idx', str(answer_idx))
        return f'''
<div class="alternative-set">
  {"".join(html_alternatives)}
</div>
<input class="ah-button ah-button--primary" type="submit" name="sendButton" value="{submit_str}" disabled />
'''

    def get_tags(self, el):
        return ['choice-exercise']


class TextExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', ['short', 'medium', 'long'], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        if self.has_class(el, 'short'):
            text_widget = '<input type="text" value="" name="data"/>'
        elif self.has_class(el, 'medium'):
            text_widget = '<div class="grow-wrap"><textarea name="data"></textarea></div>'
        elif self.has_class(el, 'long'):
            text_widget = '<div class="grow-wrap"><textarea name="data"></textarea></div>'

        submit_str = _('Submit')
        return f'''
{text_widget}

<input class="ah-button ah-button--primary" type="submit" value="{submit_str}"/>
'''

    def get_tags(self, el):
        tags = ['text-exercise']

        if self.has_class(el, 'short'):
            tags.append('short-text')
        elif self.has_class(el, 'medium'):
            tags.append('medium-text')
        elif self.has_class(el, 'long'):
            tags.append('long-text')

        return tags


class SelfProgressExercise(ExerciseAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', [], *args, **kwargs)

    def create_exercise_form(self, el, submission_form):
        submit_str = _('Submit')
        mark_done_str = _('Mark as done')
        return f'''
<input type="hidden" name="data" value="OK" />
<input class="ah-button ah-button--primary" type="submit" name="{submit_str}" value="{mark_done_str}" />
'''

    def add_extra_classes(self, el):
        el.attrib['class'] += ' self-progress'
