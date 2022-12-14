import os
from pathlib import Path
import re
import json

from dotenv import load_dotenv
from mkdocs.config import base, config_options as c
from mkdocs.plugins import BasePlugin

CWD = Path.cwd()
HERE = Path(__file__).parent

load_dotenv(CWD / ".env")


class ActiveHandoutPluginConfig(base.Config):
    telemetry = c.Type(bool, default=False)
    backend_url = c.Type(str, default='')
    course_slug = c.Type(str, default='')


class ActiveHandoutPlugin(BasePlugin[ActiveHandoutPluginConfig]):
    def _setupURLs(self, config):
        BACKEND_URL = os.getenv('BACKEND_URL')
        if BACKEND_URL:
            self.config.backend_url = BACKEND_URL

        backend_url = self.config.backend_url
        if not backend_url:
            print('backend_url is not set, no server interaction will occur')
            return config
        config['backend_url'] = backend_url

        slash = ''
        if not backend_url.endswith('/'):
            slash = '/'

        config['backend_user_menu_url'] = os.getenv('BACKEND_USER_MENU_URL', f'{backend_url}{slash}user-menu')

        return config

    def on_config(self, config):
        try:
            locale = str(config['theme']['locale'])
            config['mdx_configs']['active-handout-plugins'] = {'locale': locale}
        except KeyError:
            print('No locale set, using default')

        config['markdown_extensions'].append('active-handout-plugins')

        auth0_client_id = os.getenv('AUTH0_CLIENT_ID')
        auth0_domain = os.getenv('AUTH0_DOMAIN')
        if self.config.telemetry:
            if not auth0_client_id or not auth0_domain:
                print('Disabling telemetry. Environment variables AUTH0_CLIENT_ID and/or AUTH0_DOMAIN are not set.')
                self.config.telemetry = False
            elif not self.config.course_slug:
                print('Disabling telemetry. The variable course_slug is not set. You must set it at your mkdocs.yml.')
                self.config.telemetry = False
            else:
                config['auth0'] = {
                    'AUTH0_CLIENT_ID': auth0_client_id,
                    'AUTH0_DOMAIN': auth0_domain,
                }
                config['COURSE_SLUG'] = self.config.course_slug

        active_handout_config = {
            'telemetry': self.config.telemetry,
        }
        config['active_handout'] = self._setupURLs(active_handout_config)

        self.choice_exercise_answers = {}

        return config
    
    def on_page_markdown(self, markdown, page, config, files):
        # Saves the used seed on the last line of the page. 
        # This line is later removed in on_page_content
        return markdown + "\n<!--{{seed}} REMOVE ME-->"

    def on_page_content(self, html: str, *, page, config, files):
        self.choice_exercise_answers[page.url] = {}

        seed = 0
        matches = re.findall(r'\<\!\-\-(\d+) REMOVE ME\-\-\>', html)
        if len(matches) > 0:
            seed = int(matches[0])
        
        html = re.sub(r'^(<div class\=\"admonition exercise.*\" id=)\"(.*)\">$', 
                   r'\1"\2_' f'{seed}" data-slug="{page.url}">', html, flags=re.MULTILINE)

        matches = re.findall(r'^(<div class\=\"admonition exercise choice.*\" +id=\"([\d\w\-]+)\".*>)$', html, flags=re.MULTILINE)
        for m in matches:
            if found := re.match(r'.*data-answer-idx=\"(\d+)\".*', m[0]):
                idx = found.group(1)
                self.choice_exercise_answers[page.url][m[1]] = idx

        if page.meta and page.meta.get('show_answers', True) == False:
            html = re.sub(f'data-answer-idx=\"\d+\"', '', html)
        html_without_seed = re.sub(r'\<\!\-\-.*REMOVE ME\-\-\>', '', html)
        return html_without_seed

    def on_post_build(self, *, config) -> None:
        with open('choice_exercise_answers.json', 'w') as f:
            json.dump(self.choice_exercise_answers, f)
