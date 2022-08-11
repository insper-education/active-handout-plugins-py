from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree


class ReplaceElementWith(Treeprocessor):
    def __init__(self, pattern, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern = pattern        

    def run(self, root):
        for el in root.findall(self.pattern):
            self.visit(el)

    def visit(self, el):
        raise NotImplemented()