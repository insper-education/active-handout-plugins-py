import os
from setuptools import setup, find_packages

VERSION = '0.4.3'

with open("requirements.txt") as data:
    install_requires = [
        line for line in data.read().split("\n")
        if line and not line.startswith("#")
    ]

setup(
    name="mkdocs-active-handout",
    version=VERSION,
    url='https://github.com/insper-education/active-handout-plugins-py',
    license='',
    description="MkDocs customizations for Insper's active handouts",
    author='Igor Montagner',
    author_email='igordsm@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'mkdocs.themes': [
            'active-handout-theme = active_handout_theme',
        ],
        'markdown.extensions': ['active-handout-plugins = active_handout_plugins:ActiveHandoutExtension'],
        'mkdocs.plugins': ['active-handout = active_handout_plugins.mkdocs_plugin:ActiveHandoutPlugin']
    },
    scripts=[
        os.path.join('scripts', 'post_exercise_list.py'),
    ],
    zip_safe=False
)
