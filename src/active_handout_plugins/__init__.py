from markdown import Extension
from .video import VideoAdmonition
from .pdf import PdfAdmonition

class ActiveHandoutExtension(Extension):
    """ Admonition extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        md.treeprocessors.register(VideoAdmonition(md), 'video-admonition', 15)
        md.treeprocessors.register(PdfAdmonition(md), 'pdf-admonition', 15)