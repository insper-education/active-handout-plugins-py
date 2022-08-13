from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
from .utils import AdmonitionVisitor


class ExerciseAdmonition(AdmonitionVisitor):
    def visit(self, el):
        if not self.has_class(el, ['exercise']):
            return 
        
        answer = el.find('.//div[@class="admonition answer"]')
        if answer:
            answer.attrib['style'] = 'display: none;'
        
        form = etree.SubElement(el, 'form')
        hs_code = '''
on submit
    halt the event
    if <.answer/> 
        show the previous <.answer/>
    end
    add .done to me
    hide the <input[type="submit"]/> in me
    send remember(element: me) to window
end
'''
        form.set("_", hs_code)
        form.set("class", "form-elements")
        html_form = f'''
<input type="hidden" name="data" value="OK" />
<input type="submit" name="enviar" value="Marcar como feito" />
        '''
        form.text = self.md.htmlStash.store(html_form)
