from markdown import Extension

from .question import TextQuestion
from .progress import ProgressButtons, SplitDocumentInSections
from .counter import CounterProcessor
from .video import VideoAdmonition
from .pdf import PdfAdmonition

class ActiveHandoutExtension(Extension):
    """ Admonition extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        md.treeprocessors.register(VideoAdmonition(md), 'video-admonition', 15)
        md.treeprocessors.register(PdfAdmonition(md), 'pdf-admonition', 15)
        md.treeprocessors.register(CounterProcessor(md), 'counter', 15)
        md.treeprocessors.register(ProgressButtons(md), 'progress', 15)
        md.treeprocessors.register(TextQuestion(md), 'text-questions', 15)
        md.treeprocessors.register(SplitDocumentInSections(md), 'sections', 16)