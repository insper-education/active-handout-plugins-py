from markdown import Extension

from .exercise import ExerciseAdmonition, ChoiceExercise, SelfProgressExercise, TextExercise
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

        exercise_admonition = ExerciseAdmonition(md)
        exercise_admonition.register(ChoiceExercise(md), 1)
        exercise_admonition.register(TextExercise(md), 2)
        exercise_admonition.register(SelfProgressExercise(md), 3)

        md.treeprocessors.register(VideoAdmonition(md), 'video-admonition', 15)
        md.treeprocessors.register(PdfAdmonition(md), 'pdf-admonition', 15)
        md.treeprocessors.register(CounterProcessor(md), 'counter', 15)
        md.treeprocessors.register(ProgressButtons(md), 'progress', 15)
        md.treeprocessors.register(exercise_admonition, 'choice-exercises', 15)
        md.treeprocessors.register(ParsonsQuestion(md), 'parsons-questions', 1)
        md.treeprocessors.register(SplitDocumentInSections(md), 'sections', 16)
