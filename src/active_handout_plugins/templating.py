from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from jinja2 import Environment
import random
import string


class RandomIntVariable:
    def __init__(self):
        self.new()

    def new(self, start=0, end=10):
        self.value = random.randint(start, end)
        return self.value

    def __str__(self):
        return str(self.value)


class RandomFloatVariable:
    def __init__(self):
        self.new()

    def new(self, start=0, end=10):
        sz = end - start
        self.value = sz * random.random() + start
        return self.value

    def __str__(self):
        return str(self.value)


class RandomStringVariable:
    def __init__(self):
        self.new()

    def new(self, sz=10):
        self.value = ''.join([random.choice(string.ascii_letters) for _ in range(sz)])
        return self.value

    def __str__(self):
        return str(self.value)


class Chooser:
    def __init__(self):
        pass

    def __call__(self, *args):
        return random.choice(args)


class Jinja2PreProcessor(Preprocessor):
    def __init__(self, md, custom_variables):
        super().__init__(md)
        self.custom_variables = custom_variables

    def run(self, lines):
        text = '\n'.join(lines)
        e = Environment(extensions=['jinja2.ext.do'])
        custom_template_values = {
            'choose': Chooser(),
            'seed': random.seed,
        }
        custom_template_values.update(
            {f'randint{i}': RandomIntVariable() for i in range(1, 11)}
        )
        custom_template_values.update(
            {f'randfloat{i}': RandomFloatVariable() for i in range(1, 11)}
        )
        custom_template_values.update(
            {f'randstring{i}': RandomStringVariable() for i in range(1, 11)}
        )
        custom_template_values.update(self.custom_variables)
        new_text = e.from_string(text).render(custom_template_values)

        return new_text.split('\n')
