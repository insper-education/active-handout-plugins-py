from markdown import Extension

from .l10n import init_l10n
from .admonition import AdmonitionVisitorSelector
from .exercise import ChoiceExercise, SelfProgressExercise, TextExercise
from .progress import ProgressButtons, SplitDocumentInSections
from .counter import CounterProcessor
from .video import VideoAdmonition
from .pdf import PdfAdmonition
from .parsons import ParsonsExercise
from .templating import Jinja2PreProcessor


class ActiveHandoutExtension(Extension):
    """ Admonition extension for Python-Markdown. """
    config = {
        'locale': ['en', 'locale should be the same as for the theme'],
        'custom_variables': [{}, 'Dictionacy mapping variable names to use in Jinja templating extension'],
    }

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        init_l10n(self.getConfig('locale'))

        exercise_admonitions = AdmonitionVisitorSelector(md)
        exercise_admonitions.register(ChoiceExercise(md), 3)
        exercise_admonitions.register(TextExercise(md), 2)
        exercise_admonitions.register(ParsonsExercise(md), 2)
        exercise_admonitions.register(SelfProgressExercise(md), 1)

        md.treeprocessors.register(VideoAdmonition(md), 'video-admonition', 15)
        md.treeprocessors.register(PdfAdmonition(md), 'pdf-admonition', 15)
        md.treeprocessors.register(CounterProcessor(md), 'counter', 15)
        md.treeprocessors.register(ProgressButtons(md), 'progress', 15)
        md.treeprocessors.register(exercise_admonitions, 'exercises', 15)
        md.treeprocessors.register(SplitDocumentInSections(md), 'sections', 16)

        md.preprocessors.register(Jinja2PreProcessor(md, self.getConfig('custom_variables')), 'templating', 1000000000)
