from markdown import Extension

from .admonition import AdmonitionVisitorSelector
from .exercise import ChoiceExercise, SelfProgressExercise, TextExercise
from .progress import ProgressButtons, SplitDocumentInSections
from .counter import CounterProcessor
from .video import VideoAdmonition
from .pdf import PdfAdmonition
from .parsons import ParsonsQuestion


class ActiveHandoutExtension(Extension):
    """ Admonition extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        exercise_admonitions = AdmonitionVisitorSelector(md)
        exercise_admonitions.register(ChoiceExercise(md), 3)
        exercise_admonitions.register(TextExercise(md), 2)
        exercise_admonitions.register(SelfProgressExercise(md), 1)

        md.treeprocessors.register(VideoAdmonition(md), 'video-admonition', 15)
        md.treeprocessors.register(PdfAdmonition(md), 'pdf-admonition', 15)
        md.treeprocessors.register(CounterProcessor(md), 'counter', 15)
        md.treeprocessors.register(ProgressButtons(md), 'progress', 15)
        md.treeprocessors.register(exercise_admonitions, 'exercises', 15)
        md.treeprocessors.register(ParsonsQuestion(md), 'parsons-questions', 1)
        md.treeprocessors.register(SplitDocumentInSections(md), 'sections', 16)
