from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import re

from .utils import ReplaceElementWith

class VideoAdmonition(ReplaceElementWith):
    def __init__(self, *args, **kwargs):
        super().__init__("div[@class='admonition video']", *args, **kwargs)
        self.re = re.compile(r'https?:\/\/(www\.)?youtube\.com\/watch?.*v=(.*)&?.*')

    def visit(self, el):
        img_el = el.find("p/img")
        if not img_el is None:
            src = img_el.attrib['src']
            m = self.re.match(src)
            if m:
                html = f'<iframe width="100%" height="500" type="text/html" src="https://www.youtube.com/embed/{m.group(2)}?autoplay=0"></iframe>'
            else:
                html = f'<video width="100%" src="{src}" />'

            video_el = etree.fromstring(html)
            el.clear()
            el.append(video_el)