import os
import sys
import django
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Charity Platform'
copyright = '2026, Bubu Bebe'
author = 'Bubu Bebe'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('../../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'charity_platform.settings'
django.setup()


def skip_django_garbage(app, what, name, obj, skip, options):
    excluded_names = [
        "DoesNotExist",
        "MultipleObjectsReturned",
        "NotUpdated",
        "objects",
    ]

    if name in excluded_names:
        return True

    if not obj.__doc__:
        return True

    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_django_garbage)


autodoc_member_order = 'bysource'

autodoc_typehints = 'none'