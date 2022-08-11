from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import html

from .utils import AdmonitionVisitor


class ProgressButtons(AdmonitionVisitor):
    def visit(self, el):
        if not 'progress' in el.attrib['class']:
            return 
        
        title_p = el.find("p[@class='admonition-title']")

        hs_code = html.escape("""
on click 
    add .show to the next <section/> 
    hide me
    halt the event
end""")

        html_button = f'<a href="" class="md-button md-button--primary" _="{hs_code}"> {title_p.text} </a>'
        el.clear()
        el.append(etree.fromstring(html_button))


class SplitDocumentInSections(Treeprocessor):
    def run(self, root):
        current_section = []
        sections = []
        for el in root:
            current_section.append(el)
            if 'class' in el.attrib and 'progress' in el.attrib['class']:
                sections.append(current_section)
                current_section = []
        
        sections.append(current_section)
        for section in sections:
            sec_element = etree.SubElement(root, 'section')
            sec_element.attrib["class"] = "progress-section"
            for el in section:
                root.remove(el)
                sec_element.append(el)
