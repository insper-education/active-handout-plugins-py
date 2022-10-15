#!/bin/bash
pybabel extract --project=Active-Handout --copyright-holder=Active-Handout --no-wrap --version=0.1 --mapping-file ./babel.cfg --output-file ./active_handout_theme/messages.pot ./active_handout_theme
pybabel update --ignore-obsolete --update-header-comment --input-file ./active_handout_theme/messages.pot --output-dir ./active_handout_theme/locales --locale pt_BR
