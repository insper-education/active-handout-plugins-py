from pathlib import Path
from mkdocs.plugins import BasePlugin
import yaml


def load_author(author_dir):
    try:
        with open(author_dir / 'meta.yml', encoding='utf-8') as f:
            meta = yaml.load(f, Loader=yaml.Loader)
        if meta.get('name'):
            meta['name_by_lines'] = '<br/>'.join([
                name.strip() for name in meta['name'].split() if name.strip()
            ])
        if (author_dir / 'avatar.jpeg').is_file():
            meta['avatar'] = f'autores/{author_dir.name}/avatar.jpeg'
        return meta
    except FileNotFoundError:
        return None


def load_authors(authors_dir):
    author_dirs = [d for d in authors_dir.iterdir() if d.is_dir()]
    authors = [load_author(d) for d in author_dirs]
    return sorted([a for a in authors if a], key=lambda a: a.get('name'))


class ListContributors(BasePlugin):
    def on_page_context(self, context, page, config, nav):
        if page.meta.get('template') == 'contributors.html':
            root_dir = Path(config['config_file_path']).parent
            authors_dir = root_dir / 'content' / 'agradecimentos' / 'autores'
            context['authors'] = load_authors(authors_dir)
        return context


if __name__=='__main__':
    authors = load_authors()
    print(authors)
