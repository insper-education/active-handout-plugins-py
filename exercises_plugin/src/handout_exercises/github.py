import json
from pathlib import Path
import requests
from dataclasses import dataclass
import yaml
import re


GITHUB_NO_REPLY_REGEX = r'\d+\+(.*)@users\.noreply\.github\.com'


@dataclass
class Author:
    name: str
    email: str
    username: str
    picture: str


def Author_constructor(loader, node):
    value = loader.construct_mapping(node)
    return Author(**value)


yaml.add_constructor('tag:yaml.org,2002:python/object:handout_exercises.github.Author', Author_constructor
                     )


all_authors = None


def retrieve_author(name, email, project_root):
    global all_authors
    if all_authors == None:
        try:
            with open(Path(project_root) / 'authors.yml', 'r') as f:
                all_authors = yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError:
            all_authors = {}

    key = email
    if 'noreply.github.com' in email:
        m = re.findall(GITHUB_NO_REPLY_REGEX, email)
        if len(m) > 0:
            key = m[0]

    if data := all_authors.get(key):
        return data

    resp = requests.get(f'https://api.github.com/search/users?q={email}')
    json_response = resp.json()
    if json_response.get('total_count', 0) > 0:
        author_data = json_response['items'][0]
        all_authors[email] = Author(
            name, email, author_data['login'], author_data['avatar_url'])

        with open(Path(project_root) / 'authors.yml', 'w') as f:
            yaml.dump(all_authors, f)

        return all_authors[email]

    return Author(name, email, '', '')
