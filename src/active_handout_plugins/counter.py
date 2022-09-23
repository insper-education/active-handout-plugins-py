from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree

from .utils import AdmonitionVisitor


class CounterProcessor(AdmonitionVisitor):
    TO_COUNT = ['tip', 'exercise']

    def run(self, root):
        self.counters = {adm: 0 for adm in CounterProcessor.TO_COUNT}
        super().run(root)

    def visit(self, el):
        for c in self.counters.keys():
            if c in el.attrib['class']:
                title = el.find("p[@class='admonition-title']")
                self.counters[c] += 1
                title.text = f'{title.text} {self.counters[c]}'
