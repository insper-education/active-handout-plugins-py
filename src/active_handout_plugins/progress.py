from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import html

from .utils import AdmonitionVisitor


class ProgressButtons(AdmonitionVisitor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.count = 0

    def visit(self, el):
        if not 'progress' in el.attrib['class']:
            return 
        
        title_p = el.find("p[@class='admonition-title']")

        hs_code = html.escape("""
on click 
    add .show to the next <section/> 
    hide me
    send remember(element: me) to window
    halt 
end""")

        html_button = f'<a href="" id="prog-{self.count}" class="md-button md-button--primary progress" _="{hs_code}"> {title_p.text} </a>'
        el.clear()
        el.append(etree.fromstring(html_button))
        self.count += 1


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
        for i, section in enumerate(sections):
            sec_element = etree.SubElement(root, 'section')
            sec_element.attrib["class"] = "progress-section"
            if i == 0:
                sec_element.attrib["class"] += " show"
            for el in section:
                root.remove(el)
                sec_element.append(el)