from markdown.test_tools import TestCase

class TestVideoAdmonition(TestCase):
    default_kwargs = {
            'output_format': 'html',
            'extensions': ['admonition', 'active-handout-plugins']
            }

    def test_self_report_exercise(self):
        self.maxDiff = None
        self.assertMarkdownRenders(
        self.dedent('''
            !!! exercise 
                bla bla bla **aaa** 
        '''),

        self.dedent('''
            <section class="progress-section show">
            <div class="admonition exercise self-progress" id="exercise-1">
            <p class="admonition-title">Exercise 1</p>
            <form _="
            on submit
                halt the event
                if &lt;.answer/&gt;
                    show the &lt;.answer/&gt; in me
                end
                add @disabled to &lt;input/&gt; in me
                add @disabled to &lt;textarea/&gt; in me
                add .done to closest .exercise
                hide the &lt;input[type=&quot;submit&quot;]/&gt; in me
                send remember(element: my parentElement) to window
            end
                    ">
            <p>bla bla bla <strong>aaa</strong></p>
            <div class="form-elements">
            <input type="hidden" name="data" value="OK" />
            <input class="ah-button ah-button--primary" type="submit" name="Submit" value="Mark as done" />
            </div>
            </form>
            </div>
            </section>
          ''')
            )


