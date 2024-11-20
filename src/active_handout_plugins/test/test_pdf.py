from markdown.test_tools import TestCase

class TestPdfAdmonition(TestCase):
    default_kwargs = {
            'output_format': 'html',
            'extensions': ['admonition', 'active-handout-plugins']
            }

    def test_pdf_admonition(self):
        self.assertMarkdownRenders(
            self.dedent('''
            !!! pdf 
                ![nada aqui](arquivo.pdf)

            '''),

          self.dedent('''
            <section class="progress-section show">
            <div><center><embed height="300" src="arquivo.pdf" type="application/pdf" width="80%"></embed></center></div>
            </section>
          ''')
            )

 
