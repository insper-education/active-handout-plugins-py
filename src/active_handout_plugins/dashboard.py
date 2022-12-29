from .admonition import AdmonitionVisitor
from .l10n import gettext as _


class DashboardAdmonition(AdmonitionVisitor):
    def visit(self, el):
        if not 'dashboard' in el.attrib['class']:
            return

        el.clear()

        el.attrib['class'] = 'dashboard-container'
