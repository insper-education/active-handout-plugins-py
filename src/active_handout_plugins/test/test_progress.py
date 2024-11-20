from markdown.test_tools import TestCase

class TestProgressAdmonition(TestCase):
    default_kwargs = {
            'output_format': 'html',
            'extensions': ['admonition', 'active-handout-plugins']
            }

    def test_no_progress(self):
        self.assertMarkdownRenders(
            self.dedent('''
            só texto aqui!
            '''),

          self.dedent('''
            <section class="progress-section show">
            <p>só texto aqui!</p>
            </section>
          ''')
            )
    
    def test_one_progress(self):
        self.maxDiff = None
        self.assertMarkdownRenders(
            self.dedent('''
            texto antes progress

            !!! progress
                bla

            texto pós progress
            '''),

          self.dedent('''
            <section class="progress-section show">
            <p>texto antes progress</p>
            <div>
            <div class="ah-progress-container"><button _=" on click     add .show to the next &lt;section/&gt;     hide closest .ah-progress-container     send remember(element: me) to window     halt end" class="ah-button ah-button--primary progress" id="prog-0"> Progress </button></div>
            </div>
            </section>
            <section class="progress-section">
            <p>texto pós progress</p>
            </section>
          ''')
            )

    def test_two_progress(self):
        self.maxDiff = None
        self.assertMarkdownRenders(
            self.dedent('''
            texto antes progress

            !!! progress
                bla

            texto pós progress

            !!! progress
                texto2

            Texto final!
            '''),

          self.dedent('''
            <section class="progress-section show">
            <p>texto antes progress</p>
            <div>
            <div class="ah-progress-container"><button _=" on click     add .show to the next &lt;section/&gt;     hide closest .ah-progress-container     send remember(element: me) to window     halt end" class="ah-button ah-button--primary progress" id="prog-0"> Progress </button></div>
            </div>
            </section>
            <section class="progress-section">
            <p>texto pós progress</p>
            <div>
            <div class="ah-progress-container"><button _=" on click     add .show to the next &lt;section/&gt;     hide closest .ah-progress-container     send remember(element: me) to window     halt end" class="ah-button ah-button--primary progress" id="prog-1"> Progress </button></div>
            </div>
            </section>
            <section class="progress-section">
            <p>Texto final!</p>
            </section>
          ''')
            )
