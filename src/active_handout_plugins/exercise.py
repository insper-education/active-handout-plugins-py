from .question import QuestionAdmonition


class ExerciseAdmonition(QuestionAdmonition):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__('exercise', [], *args, **kwargs)

    def create_question_form(self, el, submission_form):
        return '''
<input type="hidden" name="data" value="OK" />
<input type="submit" name="enviar" value="Marcar como feito" />
'''
