import os
from pathlib import Path

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

        if self.config.telemetry:
            if not self.config.course_slug:
                print('Disabling telemetry. The variable course_slug is not set. You must set it at your mkdocs.yml.')
                self.config.telemetry = False
            else:
                config['COURSE_SLUG'] = self.config.course_slug

        active_handout_config = {
            'telemetry': self.config.telemetry,
        }
        config['active_handout'] = self._setupURLs(active_handout_config)

        return config
