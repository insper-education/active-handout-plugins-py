from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import re

from .utils import ReplaceElementWith

class PdfAdmonition(ReplaceElementWith):
    def __init__(self, *args, **kwargs):
        super().__init__("div[@class='admonition pdf']", *args, **kwargs)

    def visit(self, el):
        img_el = el.find("p/img")
        if not img_el is None:
            src = img_el.attrib['src']
            html = f'<center><embed width="80%" height="300" type="application/pdf" src="{src}" /></center>'
            pdf_el = etree.fromstring(html)
            el.clear()
            el.append(pdf_el)