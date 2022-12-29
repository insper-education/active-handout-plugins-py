"""
Hacks to make unittest work desirably.

VSCode + Python + Django + unittest integration is currently broken.
Django tests can be run using `python3 manage.py test` but this is not enough as VSCode unittest
runner only uses `python3 -m unittest`.

The purpose of this file is to simulate what the manage script is doing before any tests are run.
The trick is to make this load first when unittest does test discovery, hence the path `_unittest`.

This clearly cannot work when directly pointing to a test since test discovery is not used,
for example `python3 -m unittest server.component.test`.
However VSCode points to target tests differently and discovery still gets run making this work.

This all hopefully becomes obsolete if Django support is added to VSCode Python.
The issue: https://github.com/microsoft/vscode-python/issues/73
"""

import inspect
import os

import django
from django.conf import settings
from django.test.utils import get_runner


def _check_stack() -> bool:
    """
    Dig stack for the filepath of the script that imports this file.

    Return True if improting and invoking scripts are as expected.
    """
    # Skip first two calls which are this module and this function
    for frame in inspect.stack()[2:]:
        # Skip internal libraries which start with <
        if frame.filename[0] != "<":
            importing_script = frame.filename
            break
    else:
        raise RuntimeError("Importing script not found")

    # Unittest loader should be used
    if not importing_script.endswith('unittest/loader.py'):
        return False

    # Django manage script uses the same loader, so check for that as well and skip if used
    first_invoking_script = inspect.stack()[-1].filename
    if first_invoking_script.endswith('manage.py'):
        return False

    return True


# This script should only be imported, so ignore direct execute
if __name__ == "__main__":
    pass

# Only allow this hack to work with unittest loader
elif _check_stack():
    # Setup Django for testing
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    django.setup()
    settings.ALLOWED_HOSTS += ["testserver"]

    # Setup test database for testing
    get_runner(settings)(interactive=False).setup_databases()
