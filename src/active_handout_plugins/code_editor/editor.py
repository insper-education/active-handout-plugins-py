import re
from ..admonition import AdmonitionVisitor
from .utils import extract_files, remove_admonition_title


class CodeEditorAdmonition(AdmonitionVisitor):
    def visit(self, el):
        if 'code-editor' not in el.attrib['class']:
            return

        remove_admonition_title(el)
        files = extract_files(el, self.md.htmlStash)

        editors = ''
        filenames = ''
        is_first = True
        for filename, file_data in files.items():
            tab_classes = 'tab'
            editor_classes = 'file-content'
            if file_data['is_hidden']:
                editor_classes += ' hidden-file'
            else:
                lock_icon = ''
                readonly = 'false'
                if is_first and not file_data['is_readonly']:
                    tab_classes += ' active'
                    editor_classes += ' active'
                    is_first = False
                if file_data['is_readonly']:
                    readonly = 'true'
                    lock_icon = '<svg class="svg-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>'

                filenames += f'<li class="{ tab_classes }">{ lock_icon }{ filename }</li>'
            editors += f'<div class="{ editor_classes }" data-readonly="{ readonly }" data-language="{ file_data["language"] }" data-filename="{ filename }">{ file_data["code"] }</div>'

        editor_html = f'''
        <div class="file-editor">
            <ul class="file-tab">{filenames}</ul>
            <div class="file-content-container">
                { editors }
            </div>
        </div>
        '''
        el.attrib['class'] = re.sub('(?=\s*)admonition(\s|$)', '', el.attrib['class'])
        el.text = self.md.htmlStash.store(editor_html)
