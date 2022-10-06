from markdown.treeprocessors import Treeprocessor


class FootnoteTreeprocessor(Treeprocessor):
    def run(self, root):
        aside = root.find(".//aside[@class='ah-footnote-aside']")
        print('ASDASDASD', root)
