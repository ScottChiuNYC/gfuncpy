# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
from sphinx.ext.apidoc import main

sys.path.insert(0, os.path.abspath('../..'))


### for RTD to run apidoc automatically, code from https://github.com/readthedocs/readthedocs.org/issues/1139

def run_apidoc(_):
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(cur_dir, '../..', 'gfuncpy')
    main(['-e', '-o', cur_dir, module, '--force'])        # cur_dir is the output path *.rst will be in

def setup(app):
    app.connect('builder-inited', run_apidoc)


project = 'GFuncPy'
copyright = '2025, beginnerSC'
author = 'beginnerSC'
release = '0.1.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [  'nbsphinx', 
                'sphinx.ext.autodoc', 
                'sphinx.ext.napoleon',
                'sphinx.ext.mathjax', 
                'sphinx.ext.viewcode', 
                'sphinx_copybutton', 
                'sphinx_rtd_dark_mode'   # for sphinx_rtd_theme only
             ]

default_dark_mode = False

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# import pydata_sphinx_theme            # pydata theme is not working well with equations, so switching back to sphinx_rtd_theme
# html_theme = "pydata_sphinx_theme"

import sphinx_rtd_theme             # if this is commented out, the sphinx_rtd_dark_mode extension will have to be commented out as well
html_theme = "sphinx_rtd_theme"

# html_theme = 'alabaster'
html_static_path = ['_static']

master_doc = 'index'
nbsphinx_allow_errors = True
nbsphinx_execute = 'never'