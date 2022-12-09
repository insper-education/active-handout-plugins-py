## Environment Variables

You can set the following variables to override some settings:

- `BACKEND_URL`: change the backend url (useful for backend development)
- `BACKEND_USER_MENU_URL`: set the user menu url (default: `BACKEND_URL/api/user-menu`)

## Compiling SCSS and JS assets

Never modify the `assets/js` or `assets/css` folders. You should change the files under `assets_src` and then compile them.

When you are first compiling the assets locally, install the dependencies with:

    $ yarn

Then, during development, run:

    $ yarn start

Finally, to build the optimized version:

    $ yarn build

## Watching changes in the plugin from some other project

You will probably test your changes in this project with some other mkdocs project with your contents. Install the local repository with:

    $ pip install -e PATH_TO_THIS_DIR

Then, to serve mkdocs:

    $ mkdocs serve --watch PATH_TO_THIS_DIR
