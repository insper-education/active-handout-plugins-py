import os
import re
from mkdocs.plugins import BasePlugin

USE_LOCAL_JS = int(os.environ.get('USE_LOCAL_JS', '0'))
IGNORE_PATH = os.environ.get('IGNORE_PATH')

class LocalReport(BasePlugin):
    def __get_key_if_exists(self, config, *args):
        curr = config
        for k in args:
            curr = curr[k]

        return curr

    def __set_key_if_exists(self, config, new_value, *args):
        curr = config
        for k in args[:-1]:
            curr = curr[k]

        curr[args[-1]] = new_value

    def __replace_url_by_localhost_key(self, config, *args):
        try:
            value = self.__get_key_if_exists(config, *args)
            new_value = 'http://localhost:8080/' + '/'.join(value.split('/')[3:])
            self.__set_key_if_exists(config, new_value, *args)
        except KeyError:
            pass

    def on_config(self, config):
        site_url = config['site_url']
        if 'localhost' in site_url or '127.0.0.1' in site_url:
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'report', 'api-base')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'report', 'url')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'auth', 'email-password-url')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'auth', 'login-url')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'auth', 'reset-password-url')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'auth', 'url')
            self.__replace_url_by_localhost_key(config, 'extra', 'ihandout_config', 'auth', 'user-url')

        if USE_LOCAL_JS:
            for i, js in enumerate(config['extra_javascript']):
                if 'cdn.jsdelivr.net/gh/insper-education/active-handout-plugins-js' in js:
                    config['extra_javascript'][i] = 'http://localhost:9000/plugin-bundle.js'

        return config

    def on_files(self, files, config):
        if not IGNORE_PATH:
            return files

        pattern = re.compile(IGNORE_PATH)
        for file in files:
            if pattern.match(file.src_path):
                files.remove(file)
        return files
