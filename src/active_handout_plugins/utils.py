from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree


class AdmonitionVisitor(Treeprocessor):
    def run(self, root):
        for el in root.findall(".//p[@class='admonition-title']/.."):
            self.visit(el)

    def visit(self, el):
        raise NotImplemented()