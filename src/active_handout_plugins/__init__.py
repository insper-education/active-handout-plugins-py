from markdown import Extension
from collections import namedtuple

from .l10n import init_l10n
# Keep AdmonitionVisitor here so it's easier to import it in other project
from .admonition import AdmonitionVisitorSelector, AdmonitionVisitor
# Keep ExerciseAdmonition here so it's easier to import it in other project
from .exercise import ChoiceExercise, SelfProgressExercise, TextExercise, ExerciseAdmonition
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
        self._register_treeprocessors(md)

        md.preprocessors.register(Jinja2PreProcessor(md, self.getConfig('custom_variables')), 'templating', 1000000000)

    def _register_exercise_visitors(self, exercise_admonitions, md):
        for weight, visitor_builders in _registered_visitors.items():
            for visitor_builder in visitor_builders:
                exercise_admonitions.register(visitor_builder(md), weight)

    def _register_treeprocessors(self, md):
        for builder, name, priority in _registered_processors:
            md.treeprocessors.register(builder(md), name, priority)


_registered_visitors = {}
def register_exercise_visitor_builder(visitor_builder, weight):
    _registered_visitors.setdefault(weight, set()).add(visitor_builder)


_registered_processors = []
def register_treeprocessor_builder(processor_builder, name, priority):
    _registered_processors.append((processor_builder, name, priority))
