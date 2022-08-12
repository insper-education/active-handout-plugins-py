import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor


class TextQuestion(AdmonitionVisitor):
    def visit(self, el):
        if 'question' not in el.attrib['class']:
            return
        
        title = el.find('p/[@class="admonition-title"]')
        answer = el.find('.//div[@class="admonition answer"]')
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
end
        '''
        submission_form.set('_', hs_code)
        for par in content:
            el.remove(par)
            submission_form.append(par)

        html_elements = f'''
<input type="text" value="" name="data"/>

<input type="submit" value="Enviar"/>
'''
        form_elements = etree.SubElement(submission_form, 'div')
        form_elements.set("class", "form-elements")
        form_elements.text = self.md.htmlStash.store(html_elements)

        el.remove(answer)
        submission_form.append(answer)
