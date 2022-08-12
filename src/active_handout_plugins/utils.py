from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree


class AdmonitionVisitor(Treeprocessor):
    def has_class(self, el, classes_to_search):
        el_classes = el.get("class", "").split()
        return len([cls for cls in el_classes if cls in classes_to_search]) > 0

    def run(self, root):
        for el in root.findall(".//p[@class='admonition-title']/.."):
            self.visit(el)

    def visit(self, el):
        raise NotImplemented()