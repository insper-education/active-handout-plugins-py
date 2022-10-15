#!/bin/bash
pybabel extract --project=Active-Handout --copyright-holder=Active-Handout --no-wrap --version=0.1 --mapping-file src/babel.cfg --output-file src/active_handout_theme/messages.pot .
pybabel update --ignore-obsolete --update-header-comment --input-file src/active_handout_theme/messages.pot --output-dir src/active_handout_theme/locales --locale pt_BR
